// dashboard.js

// Highlight negative installment amounts in red
document.querySelectorAll('.installment-amount').forEach(el => {
  el.classList.add('neg');
});

// Auto-refresh upcoming renewals every 5 mins (optional)
// setTimeout(() => location.reload(), 300000);