// Nepal Education Platform — global JS
// Loaded on every page via base.html

(function () {
  'use strict';

  // Auto-dismiss flash alerts after 4 seconds
  document.querySelectorAll('.alert:not(.alert-permanent)').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 500);
    }, 4000);
  });

  // Confirm dangerous buttons
  document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm(btn.dataset.confirm)) e.preventDefault();
    });
  });
})();
