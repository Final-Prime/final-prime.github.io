document.querySelectorAll("[data-frontier-tabs]").forEach((container) => {
  const tabs = [...container.querySelectorAll("[data-pareto-tab]")];
  const panels = [...container.querySelectorAll("[data-pareto-panel]")];

  const activate = (tab, moveFocus = true) => {
    tabs.forEach((candidate) => {
      const selected = candidate === tab;
      candidate.setAttribute("aria-selected", String(selected));
      candidate.tabIndex = selected ? 0 : -1;
      const panel = panels.find((item) => item.id === candidate.getAttribute("aria-controls"));
      if (panel) panel.hidden = !selected;
    });
    if (moveFocus) tab.focus();
  };

  container.dataset.tabsReady = "";
  activate(tabs.find((tab) => tab.getAttribute("aria-selected") === "true") || tabs[0], false);

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(tab, false));
    tab.addEventListener("keydown", (event) => {
      let next = index;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = tabs.length - 1;
      else return;
      event.preventDefault();
      activate(tabs[next]);
    });
  });

  container.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && document.activeElement?.matches(".pareto-point")) {
      document.activeElement.blur();
    }
  });
});
