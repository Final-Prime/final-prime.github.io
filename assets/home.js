(() => {
  "use strict";

  const demoTrack = document.querySelector("[data-demo-track]");
  const trackState = document.querySelector("[data-track-state]");
  const trackOwner = document.querySelector("[data-track-owner]");
  const trackOutcomes = document.querySelector("[data-track-outcomes]");
  const trackCheck = document.querySelector("[data-track-check]");

  const isHomepage = location.pathname === "/" || location.pathname.endsWith("/index.html");
  if (isHomepage && "IntersectionObserver" in window) {
    const sectionMap = [
      [document.querySelector("#index"), "/index/"],
      [document.querySelector(".system-feature"), "/systems/"],
      [document.querySelector(".review-section"), "/thought/"],
      [document.querySelector("#contact"), "/#contact"]
    ].filter(([section]) => section);
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
      const activeRoute = active && active[1] > 0 ? active[0] : "";
      setCurrentNav(activeRoute);
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
    boundary.setAttribute("role", "group");
    boundary.setAttribute("aria-label", "Access boundary");
    boundary.innerHTML = '<div><span>PUBLIC</span><strong>Capability surface</strong></div><div><span>PRIVATE</span><strong>Implementation + research</strong></div>';
    actions?.before(boundary);
    inspector.classList.add("is-enhanced");
  }

  const trackingCard = document.querySelector(".tracking-card");
  let primaryStatus = null;
  let primaryState = null;
  let primaryNote = null;
  let outcomeNodes = [];
  if (trackingCard && !trackingCard.classList.contains("is-enhanced")) {
    const dl = trackingCard.querySelector("dl");
    const primary = document.createElement("div");
    primary.className = "tracking-primary";
    primary.setAttribute("role", "status");
    primary.setAttribute("aria-live", "off");
    primary.setAttribute("aria-atomic", "true");
    primary.innerHTML = '<span>Current state</span><strong data-track-state-primary>Under review</strong><p data-track-note>Final Prime owns the next move.</p>';
    const branch = document.createElement("div");
    branch.className = "tracking-branch";
    branch.setAttribute("role", "group");
    branch.setAttribute("aria-label", "Potential next states");
    branch.innerHTML = '<span class="tracking-origin" aria-hidden="true"></span><div class="tracking-outcomes"><span>Clarification required</span><span>Qualified</span><span>Proposal issued</span></div>';
    dl?.before(primary, branch);
    dl?.classList.add("tracking-metrics");
    trackingCard.classList.add("is-enhanced");
    primaryStatus = primary;
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

  const updateText = (node, text) => {
    if (node && node.textContent !== text) node.textContent = text;
  };

  const renderTracking = item => {
    updateText(trackState, item.state);
    updateText(primaryState, item.state);
    updateText(primaryNote, item.note);
    updateText(trackOwner, item.owner);
    updateText(trackOutcomes, item.outcomes);
    updateText(trackCheck, "Interface example");
    outcomeNodes.forEach((node, index) => node.classList.toggle("is-active", index === item.active));
  };

  renderTracking(trackingStates[0]);
  if (demoTrack) {
    demoTrack.textContent = "Advance state preview";
    demoTrack.addEventListener("click", () => {
      primaryStatus?.setAttribute("aria-live", "polite");
      trackingIndex = (trackingIndex + 1) % trackingStates.length;
      renderTracking(trackingStates[trackingIndex]);
    });
    demoTrack.hidden = false;
  }
})();
