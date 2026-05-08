// budgets.js

// Animate progress bars on load
window.addEventListener('load', () => {
  document.querySelectorAll('.progress-bar[data-pct]').forEach(bar => {
    bar.style.width = '0';
    requestAnimationFrame(() => {
      setTimeout(() => {
        bar.style.width = Math.min(parseFloat(bar.dataset.pct), 100) + '%';
      }, 80);
    });
  });
});

// Auto-submit month/year form on change
document.querySelectorAll('.month-select select').forEach(sel => {
  sel.addEventListener('change', () => sel.closest('form').submit());
});