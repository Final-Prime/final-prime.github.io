(() => {
  "use strict";

  const nav = document.querySelector("[data-dossier-nav]");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (nav) {
    const rail = nav.querySelector(".shell");
    const links = [...nav.querySelectorAll('a[href^="#"]')];
    const entries = links.map(link => {
      const id = link.getAttribute("href")?.slice(1);
      const section = id ? document.getElementById(id) : null;
      return section ? { link, section } : null;
    }).filter(Boolean);

    let activeId = "";
    let frame = 0;

    const stickyOffset = () => {
      const rootStyle = getComputedStyle(document.documentElement);
      const headerHeight = Number.parseFloat(rootStyle.getPropertyValue("--header-height")) || 0;
      return headerHeight + nav.offsetHeight + 18;
    };

    const activationOffset = () => {
      const sticky = stickyOffset();
      return Math.max(sticky, Math.min(window.innerHeight * 0.34, sticky + 180));
    };

    const syncRailState = () => {
      if (!rail) return;
      const maxScroll = Math.max(0, rail.scrollWidth - rail.clientWidth);
      nav.classList.toggle("has-overflow", maxScroll > 1);
      nav.classList.toggle("at-start", rail.scrollLeft <= 1);
      nav.classList.toggle("at-end", rail.scrollLeft >= maxScroll - 1);
    };

    const revealActiveLink = (link, behavior = reducedMotion ? "auto" : "smooth") => {
      if (!rail || rail.scrollWidth <= rail.clientWidth + 1) return;
      const left = link.offsetLeft;
      const right = left + link.offsetWidth;
      const visibleLeft = rail.scrollLeft;
      const visibleRight = visibleLeft + rail.clientWidth;
      if (left >= visibleLeft + 8 && right <= visibleRight - 8) return;
      const target = Math.max(0, left - (rail.clientWidth - link.offsetWidth) / 2);
      rail.scrollTo({ left: target, behavior });
    };

    const setActive = id => {
      if (!id) return;
      const changed = id !== activeId;
      activeId = id;
      entries.forEach(({ link, section }) => {
        if (section.id === id) {
          link.setAttribute("aria-current", "location");
          if (changed) revealActiveLink(link);
        } else {
          link.removeAttribute("aria-current");
        }
      });
    };

    const updateDossierNavigation = () => {
      frame = 0;
      if (!entries.length) return;
      const marker = window.scrollY + activationOffset();
      let active = entries[0];
      entries.forEach(entry => {
        if (entry.section.offsetTop <= marker) active = entry;
      });
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
        active = entries[entries.length - 1];
      }
      setActive(active.section.id);

      const first = entries[0].section.offsetTop;
      const last = entries[entries.length - 1].section;
      const end = Math.max(first + 1, last.offsetTop + last.offsetHeight - window.innerHeight);
      const ratio = Math.min(1, Math.max(0, (window.scrollY + stickyOffset() - first) / (end - first)));
      nav.style.setProperty("--dossier-progress", ratio.toFixed(4));
      syncRailState();
    };

    const requestNavigationUpdate = () => {
      if (frame) return;
      frame = requestAnimationFrame(updateDossierNavigation);
    };

    links.forEach(link => {
      link.addEventListener("focus", () => revealActiveLink(link, "auto"));
      link.addEventListener("click", () => {
        const id = link.getAttribute("href")?.slice(1);
        if (id) setActive(id);
        requestNavigationUpdate();
      });
    });
    rail?.addEventListener("scroll", syncRailState, { passive: true });
    window.addEventListener("scroll", requestNavigationUpdate, { passive: true });
    window.addEventListener("resize", requestNavigationUpdate, { passive: true });
    window.addEventListener("hashchange", requestNavigationUpdate);
    updateDossierNavigation();
  }

  const evidenceList = document.querySelector("[data-evidence-list]");
  const evidenceToolbar = document.querySelector("[data-evidence-toolbar]");

  if (evidenceList && evidenceToolbar) {
    const arcs = [...evidenceList.querySelectorAll("details.evidence-arc[data-spoiler]")];
    const lightArcs = arcs.filter(arc => arc.dataset.spoiler === "light");
    const status = evidenceToolbar.querySelector("[data-evidence-status]");
    const openLight = evidenceToolbar.querySelector("[data-evidence-open-light]");
    const collapse = evidenceToolbar.querySelector("[data-evidence-collapse]");
    let statusFrame = 0;
    let bulkUpdate = false;
    let bulkPending = 0;
    let bulkAnnouncement = "";
    let printState = [];
    let printRendering = false;

    const updateEvidenceStatus = announcement => {
      const openCount = arcs.filter(arc => arc.open).length;
      const message = announcement || `${openCount} of ${arcs.length} arcs open. Medium and heavy spoilers remain closed unless selected.`;
      if (status && status.textContent !== message) status.textContent = message;
      if (openLight) openLight.disabled = lightArcs.every(arc => arc.open);
      if (collapse) collapse.disabled = openCount === 0;
    };

    const scheduleEvidenceStatus = () => {
      if (bulkUpdate) return;
      if (statusFrame) cancelAnimationFrame(statusFrame);
      statusFrame = requestAnimationFrame(() => {
        statusFrame = 0;
        updateEvidenceStatus();
      });
    };

    const finishBulkUpdate = () => {
      if (statusFrame) cancelAnimationFrame(statusFrame);
      statusFrame = 0;
      bulkUpdate = false;
      bulkPending = 0;
      const announcement = bulkAnnouncement;
      bulkAnnouncement = "";
      updateEvidenceStatus(announcement);
    };

    const beginBulkUpdate = (targets, open, announcement) => {
      if (bulkUpdate) return;
      const changed = targets.filter(arc => arc.open !== open);
      bulkUpdate = true;
      bulkPending = changed.length;
      bulkAnnouncement = announcement;
      changed.forEach(arc => { arc.open = open; });
      if (!bulkPending) finishBulkUpdate();
    };

    arcs.forEach(arc => arc.addEventListener("toggle", () => {
      if (printRendering) return;
      if (!bulkUpdate) {
        scheduleEvidenceStatus();
        return;
      }
      bulkPending = Math.max(0, bulkPending - 1);
      if (!bulkPending) finishBulkUpdate();
    }));

    window.addEventListener("beforeprint", () => {
      printRendering = true;
      printState = arcs.map(arc => arc.open);
      arcs.forEach(arc => { arc.open = true; });
    });

    window.addEventListener("afterprint", () => {
      arcs.forEach((arc, index) => { arc.open = printState[index]; });
      requestAnimationFrame(() => {
        printRendering = false;
        updateEvidenceStatus();
      });
    });

    openLight?.addEventListener("click", () => {
      beginBulkUpdate(
        lightArcs,
        true,
        `${lightArcs.length} spoiler-light arcs expanded. Medium and heavy spoilers remain closed.`
      );
    });

    collapse?.addEventListener("click", () => {
      beginBulkUpdate(arcs, false, "All evidence arcs collapsed.");
    });

    evidenceToolbar.classList.add("is-enhanced");
    updateEvidenceStatus();
    if (openLight && collapse) evidenceToolbar.querySelector(".evidence-toolbar-actions")?.removeAttribute("hidden");
  }
})();
