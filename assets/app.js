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

})();
