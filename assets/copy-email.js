(() => {
  "use strict";

  const selectAddress = address => {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(address);
    selection.removeAllRanges();
    selection.addRange(range);
  };

  const legacyCopy = value => {
    const control = document.createElement("textarea");
    control.value = value;
    control.readOnly = true;
    control.style.cssText = "position:fixed;inset:0 auto auto:-9999px;opacity:0";
    document.body.append(control);
    control.select();
    const copied = document.execCommand("copy");
    control.remove();
    return copied;
  };

  const copyText = async value => {
    if (navigator.clipboard?.writeText) {
      try {
        await navigator.clipboard.writeText(value);
        return true;
      } catch {}
    }
    try {
      return legacyCopy(value);
    } catch {
      return false;
    }
  };

  const enhance = (host, address) => {
    const email = address.textContent.trim();
    if (!email || host.classList.contains("is-copy-ready")) return;

    const button = document.createElement("button");
    const status = document.createElement("span");
    button.className = "email-copy-button";
    button.type = "button";
    button.setAttribute("aria-label", `Copy ${email} to clipboard`);
    button.innerHTML = '<span class="email-copy-icon" aria-hidden="true"></span><span data-copy-label>Copy</span>';
    status.className = "email-copy-status";
    status.setAttribute("aria-live", "polite");
    host.append(button, status);
    host.classList.add("email-copy-suite", "is-copy-ready");

    let resetTimer;
    button.addEventListener("click", async () => {
      if (button.getAttribute("aria-busy") === "true") return;
      clearTimeout(resetTimer);
      button.classList.remove("is-copied", "is-copy-fallback");
      status.textContent = "";
      button.setAttribute("aria-busy", "true");
      const copied = await copyText(email);
      button.removeAttribute("aria-busy");
      void button.offsetWidth;
      button.classList.add(copied ? "is-copied" : "is-copy-fallback");
      button.querySelector("[data-copy-label]").textContent = copied ? "Copied" : "Selected";
      status.textContent = copied
        ? `Email address copied: ${email}`
        : `Copy was unavailable. Email address selected: ${email}`;
      if (!copied) selectAddress(address);
      resetTimer = setTimeout(() => {
        button.classList.remove("is-copied", "is-copy-fallback");
        button.querySelector("[data-copy-label]").textContent = "Copy";
      }, 2200);
    });
  };

  document.querySelectorAll(".footer-email").forEach(host => {
    const address = host.querySelector('a[href^="mailto:"]');
    if (address) enhance(host, address);
  });

  document.querySelectorAll(".contact-link").forEach(address => {
    const host = document.createElement("div");
    host.className = "contact-email-suite";
    address.before(host);
    host.append(address);
    enhance(host, address.querySelector("span") || address);
  });
})();
