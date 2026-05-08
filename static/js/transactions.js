// transactions.js

// Type filter buttons (Income / Expense / All)
document.querySelectorAll('.type-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.type-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filter = btn.dataset.type;
    document.querySelectorAll('tbody tr[data-type]').forEach(row => {
      row.style.display = (!filter || filter === 'all' || row.dataset.type === filter) ? '' : 'none';
    });
  });
});

// Category dropdown filter
document.getElementById('catFilter')?.addEventListener('change', function () {
  const val = this.options[this.selectedIndex].text.toLowerCase();
  document.querySelectorAll('tbody tr').forEach(row => {
    row.style.display = (!this.value || row.textContent.toLowerCase().includes(val)) ? '' : 'none';
  });
});

// Set today's date as default in add form
const dateInput = document.getElementById('tx_date');
if (dateInput) dateInput.valueAsDate = new Date();