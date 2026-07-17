(() => {
  "use strict";

  if (document.body.classList.contains("review-dossier-page")) return;

  const root = document.documentElement;
  const readout = document.createElement("output");
  let frame = 0;

  readout.className = "scroll-readout";
  readout.setAttribute("aria-hidden", "true");
  readout.hidden = true;
  document.body.append(readout);

  const update = () => {
    frame = 0;
    const range = root.scrollHeight - window.innerHeight;
    const visible = window.matchMedia("(min-width: 1081px)").matches && range > 160;
    readout.hidden = !visible;
    if (!visible) return;
    const ratio = Math.min(1, Math.max(0, window.scrollY / range));
    readout.value = `${Math.round(ratio * 100)}%`;
  };

  const scheduleUpdate = () => {
    if (!frame) frame = window.requestAnimationFrame(update);
  };

  window.addEventListener("scroll", scheduleUpdate, { passive: true });
  window.addEventListener("resize", scheduleUpdate, { passive: true });
  scheduleUpdate();
})();
