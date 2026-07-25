(() => {
  "use strict";

  document.documentElement.classList.replace("no-js", "js");

  const page = document.querySelector(".moonlight-peaks-page");
  if (!page) return;

  const sectionNav = page.querySelector("[data-section-nav]");
  const sectionLinks = sectionNav ? [...sectionNav.querySelectorAll("a[href^='#']")] : [];
  const sections = [...page.querySelectorAll("[data-track-section]")];

  let currentSectionId = "";

  const setCurrentLink = id => {
    if (id === currentSectionId) return;
    currentSectionId = id;

    let currentLink = null;
    sectionLinks.forEach(link => {
      if (link.getAttribute("href") === `#${id}`) {
        link.setAttribute("aria-current", "location");
        currentLink = link;
      } else {
        link.removeAttribute("aria-current");
      }
    });

    currentLink?.scrollIntoView({ block: "nearest", inline: "center" });
  };

  if ("IntersectionObserver" in window && sections.length && sectionLinks.length) {
    const visible = new Map();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) visible.set(entry.target.id, entry.intersectionRatio);
        else visible.delete(entry.target.id);
      });

      const current = [...visible.entries()].sort((a, b) => b[1] - a[1])[0];
      if (current) setCurrentLink(current[0]);
    }, {
      rootMargin: "-24% 0px -64% 0px",
      threshold: [0, 0.08, 0.2, 0.45, 0.7]
    });

    sections.forEach(section => observer.observe(section));
  }

  sectionLinks.forEach(link => {
    link.addEventListener("click", () => setCurrentLink(link.hash.slice(1)));
  });
})();
