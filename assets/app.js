(() => {
  "use strict";

  const body = document.body;
  const header = document.querySelector("[data-site-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const siteNav = document.querySelector("[data-site-nav]");
  const homeBrand = header?.querySelector('.brand[href="#top"]');
  if (homeBrand) homeBrand.setAttribute("aria-label", "Final Prime, back to top");
  const backgroundRegions = [...document.querySelectorAll("main, .site-footer")];
  const focusableSelector = ":is(a[href],button,input,select,textarea):not([disabled]),[tabindex]:not([tabindex='-1'])";
  let menuReturnFocus = null;
  const fallbackTabState = new Map();

  document.querySelectorAll("[data-current-year]")
    .forEach(element => element.textContent = new Date().getFullYear());

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

  const menuFocusables = () => [menuToggle, ...siteNav.querySelectorAll(focusableSelector)]
    .filter(element => !element.hasAttribute("disabled") && element.getClientRects().length > 0);

  const hashTarget = hash => {
    if (!hash) return null;
    try {
      return document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch {
      return null;
    }
  };

  const samePageHashTarget = anchor => {
    if (!anchor.hash) return null;
    const url = new URL(anchor.href);
    if (url.pathname !== location.pathname || url.search !== location.search) return null;
    return hashTarget(url.hash);
  };

  const focusHashTarget = target => {
    if (!target) return;
    const previousTabindex = target.getAttribute("tabindex");
    target.setAttribute("tabindex", "-1");
    requestAnimationFrame(() => {
      target.focus({ preventScroll: true });
      target.addEventListener("blur", () => {
        if (previousTabindex === null) target.removeAttribute("tabindex");
        else target.setAttribute("tabindex", previousTabindex);
      }, { once: true });
    });
  };

  const closeMenu = ({ restoreFocus = false } = {}) => {
    body.classList.remove("menu-open");
    siteNav.classList.remove("is-open");
    setBackgroundInert(false);

    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open primary navigation");

    if (restoreFocus) {
      const target = menuReturnFocus instanceof HTMLElement ? menuReturnFocus : menuToggle;
      target?.focus();
    }
    menuReturnFocus = null;
  };

  const openMenu = () => {
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
      const anchor = event.target.closest("a");
      if (!anchor) return;
      const hashTarget = samePageHashTarget(anchor);
      closeMenu();
      focusHashTarget(hashTarget);
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
    document.documentElement.classList.replace("no-js", "js");
    menuToggle.hidden = false;
  }
  document.addEventListener("click", event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const anchor = event.target.closest?.("a");
    if (!anchor || anchor.matches(".skip-link") || siteNav?.contains(anchor)) return;
    focusHashTarget(samePageHashTarget(anchor));
  });

  if (location.hash) focusHashTarget(hashTarget(location.hash));
  const brand = header.querySelector(".brand");
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  let timer;
  const glitch = () => {
    if (motion.matches) return;
    brand.classList.remove("is-glitching");
    requestAnimationFrame(() => brand.classList.add("is-glitching"));
  };
  const stopGlitch = () => brand.classList.remove("is-glitching");
  const schedule = () => {
    clearTimeout(timer);
    if (motion.matches || document.hidden) return;
    timer = setTimeout(() => {
      if (!document.querySelector(".hero-motto.is-glitching,.brand:is(:hover,:focus-visible,.is-glitching)")) glitch();
      schedule();
    }, 30000 + Math.random() * 20000);
  };
  brand.addEventListener("pointerdown", glitch);
  brand.addEventListener("pointerleave", stopGlitch);
  brand.addEventListener("animationend", () => !brand.matches(":hover") && stopGlitch());
  document.addEventListener("visibilitychange", schedule);
  schedule();
  const updateHeader = () => header.classList.toggle("is-scrolled", window.scrollY > 12);
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
})();
