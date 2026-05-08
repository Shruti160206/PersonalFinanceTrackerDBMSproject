'use strict';

/* ── Modals ── */
function openModal(id)  { document.getElementById(id)?.classList.add('open'); }
function closeModal(id) { document.getElementById(id)?.classList.remove('open'); }

// Close modal on background click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', e => {
    if (e.target === overlay) overlay.classList.remove('open');
  });
});

// Close modal on Escape key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape')
    document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open'));
});


/* ── Mobile sidebar toggle ── */
const sidebar = document.getElementById('sidebar');
const menuBtn = document.getElementById('menuBtn');

// Show hamburger button only on mobile
const mq = window.matchMedia('(max-width: 768px)');
function toggleMenuBtn(q) {
  if (menuBtn) menuBtn.style.display = q.matches ? 'flex' : 'none';
}
mq.addEventListener('change', toggleMenuBtn);
toggleMenuBtn(mq);

menuBtn?.addEventListener('click', () => sidebar?.classList.toggle('open'));

// Click outside sidebar to close on mobile
document.addEventListener('click', e => {
  if (mq.matches && sidebar?.classList.contains('open')) {
    if (!sidebar.contains(e.target) && e.target !== menuBtn) {
      sidebar.classList.remove('open');
    }
  }
});


/* ── Password show/hide ── */
document.querySelectorAll('.eye-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = btn.parentElement.querySelector('input');
    if (input) input.type = input.type === 'password' ? 'text' : 'password';
  });
});


/* ── Animate progress bars on load ── */
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


/* ── Table search ── */
document.getElementById('tableSearch')?.addEventListener('input', function () {
  const q = this.value.toLowerCase();
  document.querySelectorAll('tbody tr').forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
});


/* ── Flash auto dismiss ── */
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity .3s, transform .3s';
    el.style.opacity = '0';
    el.style.transform = 'translateY(-5px)';
    setTimeout(() => el.remove(), 300);
  }, 4000);
});


/* ── Confirm before delete ── */
document.querySelectorAll('[data-confirm]').forEach(btn => {
  btn.addEventListener('click', e => {
    if (!confirm(btn.dataset.confirm || 'Are you sure?')) e.preventDefault();
  });
});


/* ── Mark all notifications read ── */
document.getElementById('markAllRead')?.addEventListener('click', () => {
  document.querySelectorAll('.notif-item.unread').forEach(n => {
    n.classList.remove('unread');
    n.querySelector('.dot')?.remove();
  });
  document.querySelector('.notif-badge')?.remove();
});