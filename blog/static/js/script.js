// Dark mode toggle
const toggleBtn = document.getElementById("theme-toggle");
const root = document.documentElement;
const savedTheme = localStorage.getItem("theme") || "light";

root.setAttribute("data-theme", savedTheme);
toggleBtn.textContent = savedTheme === "dark" ? "☀️" : "🌙";

toggleBtn.addEventListener("click", () => {
  const current = root.getAttribute("data-theme");
  const next = current === "light" ? "dark" : "light";
  root.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
  toggleBtn.textContent = next === "dark" ? "☀️" : "🌙";
});
