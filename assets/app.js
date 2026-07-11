(() => {
  "use strict";

  const body = document.body;
  const header = document.querySelector("[data-site-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const siteNav = document.querySelector("[data-site-nav]");
  const currentYear = document.querySelector("[data-current-year]");
  const demoTrack = document.querySelector("[data-demo-track]");
  const trackState = document.querySelector("[data-track-state]");
  const trackOwner = document.querySelector("[data-track-owner]");
  const trackOutcomes = document.querySelector("[data-track-outcomes]");
  const trackCheck = document.querySelector("[data-track-check]");

  if (currentYear) {
    currentYear.textContent = String(new Date().getFullYear());
  }

  const closeMenu = ({ restoreFocus = false } = {}) => {
    body.classList.remove("menu-open");
    siteNav?.classList.remove("is-open");
    if (menuToggle) {
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.setAttribute("aria-label", "Open primary navigation");
      if (restoreFocus) menuToggle.focus();
    }
  };

  if (menuToggle && siteNav) {
    menuToggle.addEventListener("click", () => {
      const willOpen = menuToggle.getAttribute("aria-expanded") !== "true";
      body.classList.toggle("menu-open", willOpen);
      siteNav.classList.toggle("is-open", willOpen);
      menuToggle.setAttribute("aria-expanded", String(willOpen));
      menuToggle.setAttribute("aria-label", willOpen ? "Close primary navigation" : "Open primary navigation");
    });

    siteNav.addEventListener("click", (event) => {
      if (event.target.closest("a")) closeMenu();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menuToggle.getAttribute("aria-expanded") === "true") {
        closeMenu({ restoreFocus: true });
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 760) closeMenu();
    });
  }

  const updateHeader = () => header?.classList.toggle("is-scrolled", window.scrollY > 12);
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  const trackingStates = [
    ["Under review", "Final Prime", "Clarify / qualify / close"],
    ["Clarification required", "Buyer", "Answer → review resumes"],
    ["Qualified", "Final Prime", "Private scope / clear close"],
    ["Proposal issued", "Buyer", "Accept / counter / decline / expire"]
  ];
  let trackingIndex = 0;

  if (demoTrack && trackState && trackOwner && trackOutcomes && trackCheck) {
    demoTrack.addEventListener("click", () => {
      trackingIndex = (trackingIndex + 1) % trackingStates.length;
      const [state, owner, outcomes] = trackingStates[trackingIndex];
      trackState.textContent = state;
      trackOwner.textContent = owner;
      trackOutcomes.textContent = outcomes;
      trackCheck.textContent = "Interface example";
    });
  }
})();
