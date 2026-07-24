document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && document.activeElement?.matches(".plot-point")) {
    document.activeElement.blur();
  }
});
