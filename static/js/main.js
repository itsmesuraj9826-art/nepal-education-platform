/* ── Nepal Education Platform — Global JS ──────────────── */

// Sidebar toggle
document.getElementById('sidebarToggle')?.addEventListener('click', () => {
  const sb = document.getElementById('sidebar');
  if (window.innerWidth <= 768) {
    sb.classList.toggle('show');
  } else {
    sb.classList.toggle('collapsed');
  }
});

// Auto-dismiss alerts after 5 s
document.querySelectorAll('.alert').forEach(el => {
  setTimeout(() => {
    const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
    bsAlert?.close();
  }, 5000);
});

// Confirm dialogs via data-confirm attribute
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', e => {
    if (!confirm(el.dataset.confirm)) e.preventDefault();
  });
});

// DataTables default init for any table with class .dt-table
document.querySelectorAll('.dt-table').forEach(table => {
  if (typeof $ !== 'undefined' && $.fn.DataTable) {
    $(table).DataTable({ pageLength: 25, responsive: true });
  }
});

// GPS Attendance Check-In helper (called from mobile web)
window.NepalEdu = {
  checkIn(teacherId) {
    if (!navigator.geolocation) {
      alert('Geolocation not supported.');
      return;
    }
    navigator.geolocation.getCurrentPosition(pos => {
      fetch('/attendance/checkin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          teacher_id: teacherId,
          latitude:   pos.coords.latitude,
          longitude:  pos.coords.longitude,
          method:     'mobile_app',
        }),
      })
      .then(r => r.json())
      .then(d => alert(d.message || d.error))
      .catch(e => alert('Check-in failed: ' + e));
    }, err => alert('GPS error: ' + err.message));
  },

  checkOut(teacherId) {
    navigator.geolocation.getCurrentPosition(pos => {
      fetch('/attendance/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          teacher_id: teacherId,
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
        }),
      })
      .then(r => r.json())
      .then(d => alert(d.message || d.error));
    });
  }
};
