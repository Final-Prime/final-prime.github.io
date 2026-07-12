(() => {
  "use strict";

  document.documentElement.classList.add("js");

  const body = document.body;
  const header = document.querySelector("[data-site-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const siteNav = document.querySelector("[data-site-nav]");
  const homeBrand = header?.querySelector('.brand[href="#top"]');
  if (homeBrand) homeBrand.setAttribute("aria-label", "FINAL / PRIME, back to top");
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

  const currentYear = String(new Date().getFullYear());
  document.querySelectorAll("[data-current-year]").forEach(element => {
    if (element.textContent !== currentYear) element.textContent = currentYear;
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

  requestAnimationFrame(updateHeader);
  window.addEventListener("scroll", updateHeader, { passive: true });
  window.addEventListener("resize", updateHeader, { passive: true });

})();
