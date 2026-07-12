import fs from "node:fs";
import { chromium } from "playwright";

const route = "http://127.0.0.1:8000/reviews/metro-2033-redux/";
const output = "metro-score-layout-qa";
const cases = [
  { name: "desktop-1920", width: 1920, height: 1080, scale: 1 },
  { name: "desktop-1440", width: 1440, height: 1000, scale: 1 },
  { name: "desktop-min-1181", width: 1181, height: 900, scale: 1 },
  { name: "tablet-1024", width: 1024, height: 900, scale: 1 },
  { name: "mobile-390", width: 390, height: 844, scale: 1 },
  { name: "mobile-320", width: 320, height: 800, scale: 1 },
  { name: "mobile-390-text-200", width: 390, height: 844, scale: 2 },
];

fs.mkdirSync(output, { recursive: true });
const browser = await chromium.launch({ headless: true });
const failures = [];
const results = [];

try {
  for (const item of cases) {
    const context = await browser.newContext({
      viewport: { width: item.width, height: item.height },
      reducedMotion: "reduce",
    });
    const page = await context.newPage();
    const runtimeErrors = [];
    const failedAssets = [];

    page.on("pageerror", error => runtimeErrors.push(String(error)));
    page.on("console", message => {
      if (message.type() === "error") runtimeErrors.push(message.text());
    });
    page.on("response", response => {
      if (response.url().startsWith("http://127.0.0.1:8000/") && response.status() >= 400) {
        failedAssets.push(`${response.status()} ${response.url()}`);
      }
    });

    const response = await page.goto(route, { waitUntil: "networkidle" });
    if (!response || response.status() !== 200) {
      failures.push(`${item.name}: route did not return HTTP 200`);
    }

    if (item.scale === 2) {
      await page.evaluate(() => {
        document.documentElement.style.fontSize = "200%";
      });
      await page.waitForTimeout(120);
    }

    const metrics = await page.evaluate(() => {
      const title = document.querySelector("#score-title");
      const headings = [...document.querySelectorAll(".dossier-axis h3")];
      const meters = [...document.querySelectorAll(".dossier-meter")];
      const grades = [...document.querySelectorAll(".dossier-axis-body > small")];
      const headingMetrics = headings.map(node => {
        const rect = node.getBoundingClientRect();
        const lineHeight = Number.parseFloat(getComputedStyle(node).lineHeight) || rect.height;
        return {
          text: node.textContent.trim(),
          lines: rect.height / lineHeight,
          scrollWidth: node.scrollWidth,
          clientWidth: node.clientWidth,
        };
      });
      const meterTops = meters.map(node => Math.round(node.getBoundingClientRect().top * 10) / 10);
      const gradeTops = grades.map(node => Math.round(node.getBoundingClientRect().top * 10) / 10);
      return {
        viewportWidth: innerWidth,
        documentWidth: document.documentElement.scrollWidth,
        horizontalOverflow: document.documentElement.scrollWidth > innerWidth + 1,
        titleText: (title?.textContent || "").replace(/\s+/g, " ").trim(),
        titleLabel: title?.getAttribute("aria-label"),
        headingMetrics,
        meterTops,
        gradeTops,
        meterSpread: Math.max(...meterTops) - Math.min(...meterTops),
        gradeSpread: Math.max(...gradeTops) - Math.min(...gradeTops),
      };
    });

    if (metrics.horizontalOverflow) {
      failures.push(`${item.name}: horizontal overflow ${metrics.documentWidth}/${metrics.viewportWidth}`);
    }
    if (metrics.titleText !== "90 − 4 = 86.") {
      failures.push(`${item.name}: visible equation is ${JSON.stringify(metrics.titleText)}`);
    }
    if (metrics.titleLabel !== "90 minus 4 equals 86") {
      failures.push(`${item.name}: accessible equation label is missing`);
    }
    if (runtimeErrors.length) {
      failures.push(`${item.name}: runtime errors: ${runtimeErrors.join(" | ")}`);
    }
    if (failedAssets.length) {
      failures.push(`${item.name}: failed assets: ${failedAssets.join(" | ")}`);
    }

    if (item.width >= 1181) {
      const wrapped = metrics.headingMetrics.filter(metric => (
        metric.lines > 1.25 || metric.scrollWidth > metric.clientWidth + 1
      ));
      if (wrapped.length) {
        failures.push(`${item.name}: axis labels do not fit: ${JSON.stringify(wrapped)}`);
      }
      if (metrics.meterSpread > 2) {
        failures.push(`${item.name}: meter tops differ by ${metrics.meterSpread}px`);
      }
      if (metrics.gradeSpread > 2) {
        failures.push(`${item.name}: grade tops differ by ${metrics.gradeSpread}px`);
      }
    }

    await page.locator("#score").screenshot({ path: `${output}/${item.name}-score.png` });
    results.push({ ...item, metrics, runtimeErrors, failedAssets });
    await context.close();
  }
} finally {
  await browser.close();
}

fs.writeFileSync(`${output}/report.json`, JSON.stringify({ results, failures }, null, 2));
fs.writeFileSync(
  `${output}/summary.txt`,
  failures.length
    ? `FAILED\n${failures.join("\n")}\n`
    : "PASSED\nSymbolic equation, label fit, and receipt alignment verified.\n",
);

if (failures.length) process.exit(1);
