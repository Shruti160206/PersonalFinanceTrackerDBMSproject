'use strict';

/* ── Modals ── */
function openModal(id)  { document.getElementById(id)?.classList.add('open'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('open'); }

document.querySelectorAll('.modal-overlay').forEach(o => {
  o.addEventListener('click', e => { if (e.target === o) o.classList.remove('open'); });
});
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
});

/* ── Sidebar mobile toggle ── */
const sidebar = document.getElementById('sidebar');
document.getElementById('menuBtn')?.addEventListener('click', () => sidebar?.classList.toggle('open'));

/* ── Active nav link ── */
document.querySelectorAll('.nav-link[href]').forEach(a => {
  if (window.location.pathname === a.getAttribute('href')) a.classList.add('active');
});

/* ── Password show/hide ── */
document.querySelectorAll('.eye-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = btn.parentElement.querySelector('input');
    if (!input) return;
    input.type = input.type === 'password' ? 'text' : 'password';
  });
});

/* ── Animate progress bars ── */
window.addEventListener('load', () => {
  document.querySelectorAll('.progress-bar[data-pct]').forEach(bar => {
    bar.style.width = '0';
    requestAnimationFrame(() => setTimeout(() => bar.style.width = Math.min(parseFloat(bar.dataset.pct), 100) + '%', 80));
  });
});

/* ── Filter chips (type filter on table rows) ── */
document.querySelectorAll('.chip[data-filter]').forEach(chip => {
  chip.addEventListener('click', () => {
    const group = chip.dataset.group;
    if (group) document.querySelectorAll(`.chip[data-group="${group}"]`).forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    const val = chip.dataset.filter;
    const col = chip.dataset.col || 'type';
    document.querySelectorAll(`tbody tr[data-${col}]`).forEach(row => {
      row.style.display = (!val || val === 'all' || row.dataset[col] === val) ? '' : 'none';
    });
  });
});

/* ── Search table ── */
document.getElementById('tableSearch')?.addEventListener('input', function () {
  const q = this.value.toLowerCase();
  document.querySelectorAll('tbody tr').forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
});

/* ── Flash auto dismiss ── */
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateY(-5px)'; el.style.transition = '.3s'; setTimeout(() => el.remove(), 300); }, 4000);
});

/* ── Mark notifications read ── */
document.getElementById('markAllRead')?.addEventListener('click', () => {
  document.querySelectorAll('.notif-item.unread').forEach(n => { n.classList.remove('unread'); n.querySelector('.dot')?.remove(); });
  document.querySelector('.notif-badge')?.remove();
});

/* ── Confirm delete ── */
document.querySelectorAll('[data-confirm]').forEach(btn => {
  btn.addEventListener('click', e => { if (!confirm(btn.dataset.confirm)) e.preventDefault(); });
});