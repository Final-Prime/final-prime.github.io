(() => {
  "use strict";

  const motto = document.querySelector(".hero-motto");
  if (!motto) return;
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  let timer;
  const stop = () => motto.classList.remove("is-glitching");
  const play = () => {
    if (motion.matches) return;
    stop();
    requestAnimationFrame(() => motto.classList.add("is-glitching"));
  };
  const schedule = () => {
    clearTimeout(timer);
    if (motion.matches || document.hidden) {
      stop();
      return;
    }
    timer = setTimeout(() => {
      if (!motto.matches(":hover, .is-glitching") && !document.querySelector(".brand.is-glitching")) play();
      schedule();
    }, 40000 + Math.random() * 20000);
  };

  motto.addEventListener("pointerenter", play);
  motto.addEventListener("pointerdown", play);
  motto.addEventListener("animationend", event => {
    if (event.animationName === "fp-motto-complementary-glitch") stop();
  });
  document.addEventListener("visibilitychange", schedule);
  motion.addEventListener("change", schedule);
  schedule();
})();
