(() => {
  "use strict";

  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

  const body = document.body;
  const header = document.querySelector("[data-site-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const siteNav = document.querySelector("[data-site-nav]");
  const demoTrack = document.querySelector("[data-demo-track]");
  const trackState = document.querySelector("[data-track-state]");
  const trackOwner = document.querySelector("[data-track-owner]");
  const trackOutcomes = document.querySelector("[data-track-outcomes]");
  const trackCheck = document.querySelector("[data-track-check]");
  const backgroundRegions = [...document.querySelectorAll("main, .site-footer")];
  const focusableSelector = [
    "a[href]",
    "button:not([disabled])",
    "input:not([disabled])",
    "select:not([disabled])",
    "textarea:not([disabled])",
    "[tabindex]:not([tabindex='-1'])"
  ].join(",");

  let menuReturnFocus = null;
  const fallbackTabState = new Map();

  const ensureLegalNotice = () => {
    if (!document.head.querySelector('meta[name="author"]')) {
      const author = document.createElement("meta");
      author.name = "author";
      author.content = "Daniel Kenessy";
      document.head.append(author);
    }
    if (!document.head.querySelector('meta[name="copyright"]')) {
      const copyright = document.createElement("meta");
      copyright.name = "copyright";
      copyright.content = "© 2026 Daniel Kenessy";
      document.head.append(copyright);
    }
    if (!document.head.querySelector('link[rel="license"]')) {
      const license = document.createElement("link");
      license.rel = "license";
      license.href = "/legal/";
      document.head.append(license);
    }

    const footerNav = document.querySelector(".footer-nav");
    if (footerNav && !footerNav.querySelector('a[href="/legal/"]')) {
      const link = document.createElement("a");
      link.href = "/legal/";
      link.textContent = "Legal / IP";
      if (location.pathname.startsWith("/legal/")) link.setAttribute("aria-current", "page");
      footerNav.append(link);
    }

    const footerMeta = document.querySelector(".footer-meta");
    if (!footerMeta) return;

    const copyrightLine = [...footerMeta.querySelectorAll("p")].find(item => item.textContent.includes("All rights reserved."));
    if (copyrightLine) copyrightLine.innerHTML = '© <span data-current-year>2026</span> Daniel Kenessy. All rights reserved.';

    const hasLegalMark = [...footerMeta.querySelectorAll("p")].some(item => {
      return item.textContent.includes("Final Prime™ is claimed as an unregistered mark of Daniel Kenessy.");
    });
    if (!hasLegalMark) {
      const mark = document.createElement("p");
      mark.dataset.legalMark = "true";
      mark.textContent = "Final Prime™ is claimed as an unregistered mark of Daniel Kenessy.";
      footerMeta.prepend(mark);
    }

    const footer = footerMeta.closest(".site-footer");
    if (!footer?.querySelector('a[href="/legal/"]')) {
      const line = document.createElement("p");
      line.dataset.legalLink = "true";
      line.innerHTML = '<a href="/legal/">Legal / IP notice</a>';
      footerMeta.append(line);
    }
  };

  ensureLegalNotice();
  document.querySelectorAll("[data-current-year]").forEach(element => {
    element.textContent = String(new Date().getFullYear());
  });

  const setBackgroundInert = open => {
    backgroundRegions.forEach(region => {
      if ("inert" in region) {
        region.inert = open;
        return;
      }

      if (open) {
        region.setAttribute("aria-hidden", "true");
        region.querySelectorAll(focusableSelector).forEach(element => {
          fallbackTabState.set(element, element.getAttribute("tabindex"));
          element.setAttribute("tabindex", "-1");
        });
      } else {
        region.removeAttribute("aria-hidden");
        region.querySelectorAll(focusableSelector).forEach(element => {
          const previous = fallbackTabState.get(element);
          if (previous === null || previous === undefined) element.removeAttribute("tabindex");
          else element.setAttribute("tabindex", previous);
          fallbackTabState.delete(element);
        });
      }
    });
  };

  const menuFocusables = () => {
    if (!menuToggle || !siteNav) return [];
    return [menuToggle, ...siteNav.querySelectorAll(focusableSelector)].filter(element => {
      return !element.hasAttribute("disabled") && element.getClientRects().length > 0;
    });
  };

  const closeMenu = ({ restoreFocus = false } = {}) => {
    body.classList.remove("menu-open");
    siteNav?.classList.remove("is-open");
    setBackgroundInert(false);

    if (menuToggle) {
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", "Open primary navigation");
    }

    if (restoreFocus) {
      const target = menuReturnFocus instanceof HTMLElement ? menuReturnFocus : menuToggle;
      target?.focus();
    }
    menuReturnFocus = null;
  };

  const openMenu = () => {
    if (!menuToggle || !siteNav) return;
    menuReturnFocus = document.activeElement instanceof HTMLElement ? document.activeElement : menuToggle;
    body.classList.add("menu-open");
    siteNav.classList.add("is-open");
    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Close primary navigation");
    setBackgroundInert(true);
    const firstLink = siteNav.querySelector(focusableSelector);
    requestAnimationFrame(() => firstLink?.focus());
  };

  if (menuToggle && siteNav) {
    menuToggle.addEventListener("click", () => {
      const open = menuToggle.getAttribute("aria-expanded") === "true";
      if (open) closeMenu({ restoreFocus: true });
      else openMenu();
    });

    siteNav.addEventListener("click", event => {
      if (event.target.closest("a")) closeMenu();
    });

    document.addEventListener("pointerdown", event => {
      if (menuToggle.getAttribute("aria-expanded") !== "true") return;
      if (siteNav.contains(event.target) || menuToggle.contains(event.target)) return;
      closeMenu({ restoreFocus: true });
    });

    document.addEventListener("keydown", event => {
      if (menuToggle.getAttribute("aria-expanded") !== "true") return;

      if (event.key === "Escape") {
        event.preventDefault();
        closeMenu({ restoreFocus: true });
        return;
      }

      if (event.key !== "Tab") return;
      const focusables = menuFocusables();
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 760 && menuToggle.getAttribute("aria-expanded") === "true") closeMenu();
    }, { passive: true });

    window.addEventListener("pagehide", () => closeMenu());
  }

  const progress = document.createElement("div");
  progress.className = "site-progress";
  progress.setAttribute("aria-hidden", "true");
  progress.innerHTML = "<span data-scroll-progress></span>";
  header?.append(progress);
  const progressFill = progress.querySelector("[data-scroll-progress]");

  const updateHeader = () => {
    header?.classList.toggle("is-scrolled", window.scrollY > 12);
    if (!progressFill) return;
    const scrollable = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    const ratio = Math.min(1, Math.max(0, window.scrollY / scrollable));
    progressFill.style.transform = `scaleX(${ratio})`;
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
  window.addEventListener("resize", updateHeader, { passive: true });

  const isHomepage = location.pathname === "/" || location.pathname.endsWith("/index.html");
  if (isHomepage && "IntersectionObserver" in window) {
    const sectionMap = [
      [document.querySelector("#systems"), "/systems/"],
      [document.querySelector("#works"), "/works/"],
      [document.querySelector("#thought"), "/thought/"],
      [document.querySelector("#index"), "/index/"],
      [document.querySelector("#prime-access"), "/#prime-access"]
    ].filter(([section]) => section);
    const systemsFeature = document.querySelector(".system-feature");
    if (systemsFeature) sectionMap.push([systemsFeature, "/systems/"]);
    const visible = new Map();

    const setCurrentNav = route => {
      document.querySelectorAll(".site-nav a").forEach(link => {
        const href = link.getAttribute("href");
        if (href === route) link.setAttribute("aria-current", "location");
        else if (link.getAttribute("aria-current") === "location") link.removeAttribute("aria-current");
      });
    };

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const route = sectionMap.find(([section]) => section === entry.target)?.[1];
        if (route) visible.set(route, entry.intersectionRatio);
      });
      const active = [...visible.entries()].sort((a, b) => b[1] - a[1])[0];
      if (active && active[1] > 0) setCurrentNav(active[0]);
    }, { rootMargin: "-18% 0px -62% 0px", threshold: [0, 0.08, 0.25, 0.5, 0.75] });

    sectionMap.forEach(([section]) => observer.observe(section));
  }

  const domainData = [
    { state: "Mixed access", specs: [["Surface", "Selected demonstrations"], ["Core", "Private by default"], ["State", "Active / prototype"]], foot: ["Current object", "A/SYNC"] },
    { state: "Public", specs: [["Surface", "Reviewable releases"], ["Core", "Process selectively shown"], ["State", "Index prepared"]], foot: ["Primary mode", "Objects"] },
    { state: "Public", specs: [["Surface", "Long-form analysis"], ["Core", "Research trails retained"], ["State", "Editorial pipeline"]], foot: ["Primary mode", "Models"] },
    { state: "Registry", specs: [["Surface", "Object registry"], ["Core", "Canonical state"], ["State", "Continuous"]], foot: ["Primary mode", "Lineage"] }
  ];

  document.querySelectorAll(".domain").forEach((domain, index) => {
    if (domain.classList.contains("is-enhanced") || !domainData[index]) return;
    const data = domainData[index];
    const code = domain.querySelector(".domain-code");
    const legacyList = domain.querySelector("ul");
    const top = document.createElement("div");
    top.className = "domain-top";
    if (code) top.append(code);
    const state = document.createElement("span");
    state.className = "domain-state";
    state.textContent = data.state;
    top.append(state);
    domain.prepend(top);

    const specs = document.createElement("dl");
    specs.className = "domain-spec";
    specs.innerHTML = data.specs.map(([term, value]) => `<div><dt>${term}</dt><dd>${value}</dd></div>`).join("");
    legacyList?.replaceWith(specs);

    const foot = document.createElement("div");
    foot.className = "domain-foot";
    foot.innerHTML = `<span>${data.foot[0]}</span><strong>${data.foot[1]}</strong>`;
    domain.append(foot);
    domain.classList.add("is-enhanced");
  });

  const stage = document.querySelector(".object-stage");
  if (stage && !stage.classList.contains("is-enhanced")) {
    stage.innerHTML = `
      <div class="stage-topline"><span>COORDINATION FIELD / 04 INPUTS</span><strong><i aria-hidden="true"></i> TRACKED</strong></div>
      <svg class="system-map" viewBox="0 0 920 520" aria-hidden="true" focusable="false">
        <defs>
          <linearGradient id="routeFuchsia" x1="0" x2="1"><stop offset="0" stop-color="#f5054d" stop-opacity=".15"/><stop offset="1" stop-color="#f5054d" stop-opacity="1"/></linearGradient>
          <linearGradient id="routeCyan" x1="0" x2="1"><stop offset="0" stop-color="#0ae8f7" stop-opacity=".12"/><stop offset="1" stop-color="#0ae8f7" stop-opacity="1"/></linearGradient>
        </defs>
        <g class="map-grid" opacity=".45"><path d="M0 65H920M0 130H920M0 195H920M0 260H920M0 325H920M0 390H920M0 455H920"/><path d="M115 0V520M230 0V520M345 0V520M460 0V520M575 0V520M690 0V520M805 0V520"/></g>
        <g class="map-routes"><path class="route route-muted" d="M115 115C255 115 300 210 425 248"/><path class="route route-cyan" d="M115 405C255 405 310 315 425 272"/><path class="route route-muted" d="M805 115C665 115 620 210 495 248"/><path class="route route-fuchsia" d="M805 405C665 405 610 315 495 272"/><path class="route route-core" d="M460 184V336"/></g>
        <g class="map-nodes"><g transform="translate(115 115)"><circle r="14"/><circle class="node-pulse" r="25"/><text x="26" y="5">OBJECTIVE</text></g><g transform="translate(115 405)"><circle class="cyan" r="14"/><circle class="node-pulse cyan" r="25"/><text x="26" y="5">CONSTRAINT</text></g><g transform="translate(805 115)"><circle r="14"/><circle class="node-pulse" r="25"/><text x="-26" y="5" text-anchor="end">SIGNAL</text></g><g transform="translate(805 405)"><circle class="fuchsia" r="14"/><circle class="node-pulse fuchsia" r="25"/><text x="-26" y="5" text-anchor="end">OUTCOME</text></g></g>
        <g class="map-core" transform="translate(460 260)"><rect x="-78" y="-78" width="156" height="156" transform="rotate(45)"/><rect class="core-inner" x="-39" y="-39" width="78" height="78" transform="rotate(45)"/><text y="5" text-anchor="middle">A/SYNC</text></g>
        <g class="map-axis"><text x="28" y="495">INPUT STATE</text><text x="892" y="495" text-anchor="end">RESOLVED ROUTE</text></g>
      </svg>
      <div class="stage-readout"><div><span>Route</span><strong>Constraint-led</strong></div><div><span>Visibility</span><strong>Concept surface</strong></div><div><span>Internals</span><strong>Private</strong></div></div>`;
    stage.classList.add("is-enhanced");
  }

  const inspector = document.querySelector(".object-inspector");
  if (inspector && !inspector.classList.contains("is-enhanced")) {
    const code = inspector.querySelector(".inspector-code");
    if (code) {
      const top = document.createElement("div");
      top.className = "inspector-topline";
      code.before(top);
      top.append(code);
      const objectState = document.createElement("span");
      objectState.className = "object-state";
      objectState.innerHTML = '<i aria-hidden="true"></i> Prototype';
      top.append(objectState);
    }
    const actions = inspector.querySelector(".inspector-actions");
    const boundary = document.createElement("div");
    boundary.className = "access-boundary";
    boundary.setAttribute("aria-label", "Access boundary");
    boundary.innerHTML = '<div><span>PUBLIC</span><strong>Capability surface</strong></div><div><span>PRIVATE</span><strong>Implementation + research</strong></div>';
    actions?.before(boundary);
    inspector.classList.add("is-enhanced");
  }

  const trackingCard = document.querySelector(".tracking-card");
  let primaryState = null;
  let primaryNote = null;
  let outcomeNodes = [];
  if (trackingCard && !trackingCard.classList.contains("is-enhanced")) {
    const dl = trackingCard.querySelector("dl");
    const primary = document.createElement("div");
    primary.className = "tracking-primary";
    primary.innerHTML = '<span>Current state</span><strong data-track-state-primary>Under review</strong><p data-track-note>Final Prime owns the next move.</p>';
    const branch = document.createElement("div");
    branch.className = "tracking-branch";
    branch.setAttribute("aria-label", "Potential next states");
    branch.innerHTML = '<span class="tracking-origin" aria-hidden="true"></span><div class="tracking-outcomes"><span>Clarification required</span><span>Qualified</span><span>Not a fit / closed</span></div>';
    dl?.before(primary, branch);
    dl?.classList.add("tracking-metrics");
    trackingCard.classList.add("is-enhanced");
    primaryState = primary.querySelector("[data-track-state-primary]");
    primaryNote = primary.querySelector("[data-track-note]");
    outcomeNodes = [...branch.querySelectorAll(".tracking-outcomes span")];
  }

  const contactCopy = document.querySelector(".contact-copy");
  if (contactCopy && !contactCopy.querySelector(".contact-routing")) {
    const note = contactCopy.querySelector(".contact-note");
    const routing = document.createElement("dl");
    routing.className = "contact-routing";
    routing.setAttribute("aria-label", "Contact routing guidance");
    routing.innerHTML = '<div><dt>General question</dt><dd>Email reply</dd></div><div><dt>Concrete business idea</dt><dd>Qualified workspace invitation</dd></div><div><dt>Phone call</dt><dd>Not required</dd></div>';
    note?.before(routing);
  }

  const trackingStates = [
    { state: "Under review", owner: "Final Prime", outcomes: "Clarify / qualify / close", note: "Final Prime owns the next move.", active: -1 },
    { state: "Clarification required", owner: "Buyer", outcomes: "Answer, then review resumes", note: "A targeted buyer response is required.", active: 0 },
    { state: "Qualified", owner: "Final Prime", outcomes: "Private scope / clear close", note: "The private-scoping branch is available.", active: 1 },
    { state: "Proposal issued", owner: "Buyer", outcomes: "Accept / counter / decline / expire", note: "A versioned proposal is ready for decision.", active: 2 }
  ];
  let trackingIndex = 0;

  const renderTracking = item => {
    if (trackState) trackState.textContent = item.state;
    if (primaryState) primaryState.textContent = item.state;
    if (primaryNote) primaryNote.textContent = item.note;
    if (trackOwner) trackOwner.textContent = item.owner;
    if (trackOutcomes) trackOutcomes.textContent = item.outcomes;
    if (trackCheck) trackCheck.textContent = "Interface example";
    outcomeNodes.forEach((node, index) => node.classList.toggle("is-active", index === item.active));
  };

  renderTracking(trackingStates[0]);
  if (demoTrack) {
    demoTrack.textContent = "Advance state preview";
    demoTrack.addEventListener("click", () => {
      trackingIndex = (trackingIndex + 1) % trackingStates.length;
      renderTracking(trackingStates[trackingIndex]);
    });
  }
})();
