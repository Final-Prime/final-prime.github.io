(() => {
  "use strict";

  const body = document.body;
  const header = document.querySelector("[data-site-header]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const siteNav = document.querySelector("[data-site-nav]");
  const primeList = document.querySelector("[data-prime-list]");
  const nextPrimeButton = document.querySelector("[data-next-prime]");
  const primeCount = document.querySelector("[data-prime-count]");
  const primeLatest = document.querySelector("[data-prime-latest]");
  const currentYear = document.querySelector("[data-current-year]");

  if (currentYear) {
    currentYear.textContent = String(new Date().getFullYear());
  }

  const closeMenu = () => {
    body.classList.remove("menu-open");
    if (menuToggle) {
      menuToggle.setAttribute("aria-expanded", "false");
    }
  };

  if (menuToggle && siteNav) {
    menuToggle.addEventListener("click", () => {
      const isOpen = body.classList.toggle("menu-open");
      menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    siteNav.addEventListener("click", (event) => {
      if (event.target instanceof HTMLAnchorElement) {
        closeMenu();
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        closeMenu();
        menuToggle.focus();
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth > 780) {
        closeMenu();
      }
    });
  }

  const updateHeader = () => {
    if (header) {
      header.classList.toggle("is-scrolled", window.scrollY > 12);
    }
  };

  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  const isPrime = (value) => {
    if (!Number.isInteger(value) || value < 2) {
      return false;
    }
    if (value === 2) {
      return true;
    }
    if (value % 2 === 0) {
      return false;
    }

    const limit = Math.floor(Math.sqrt(value));
    for (let divisor = 3; divisor <= limit; divisor += 2) {
      if (value % divisor === 0) {
        return false;
      }
    }
    return true;
  };

  const findNextPrime = (after) => {
    let candidate = Math.max(2, after + 1);
    while (!isPrime(candidate)) {
      candidate += 1;
    }
    return candidate;
  };

  if (primeList && nextPrimeButton && primeCount && primeLatest) {
    let totalResolved = primeList.children.length;
    let latest = Number.parseInt(primeLatest.textContent || "61", 10);

    nextPrimeButton.addEventListener("click", () => {
      latest = findNextPrime(latest);
      totalResolved += 1;

      const item = document.createElement("li");
      item.textContent = String(latest);
      item.className = "is-new";
      primeList.append(item);

      window.setTimeout(() => item.classList.remove("is-new"), 520);

      while (primeList.children.length > 24) {
        primeList.firstElementChild?.remove();
      }

      primeCount.textContent = String(totalResolved);
      primeLatest.textContent = String(latest);
    });
  }
})();
