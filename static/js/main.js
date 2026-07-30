/* ============================================================
   Mini Football Manager - main.js
   Global JavaScript: sidebar toggle, modals, confirmations,
   flash auto-dismiss, AJAX helpers.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // Event Delegation for click events
  document.body.addEventListener('click', function (e) {
    
    // Sidebar Toggle
    const toggleBtn = e.target.closest('#sidebarToggle');
    if (toggleBtn) {
      e.preventDefault();
      const sidebar = document.getElementById('sidebar');
      const overlay = document.getElementById('sidebarOverlay');
      if (sidebar?.classList.contains('show')) {
        sidebar.classList.remove('show');
        overlay?.classList.remove('show');
        document.body.style.overflow = '';
      } else {
        sidebar?.classList.add('show');
        overlay?.classList.add('show');
        document.body.style.overflow = 'hidden';
      }
    }

    // Sidebar Overlay close
    if (e.target.closest('#sidebarOverlay')) {
      const sidebar = document.getElementById('sidebar');
      const overlay = document.getElementById('sidebarOverlay');
      sidebar?.classList.remove('show');
      overlay?.classList.remove('show');
      document.body.style.overflow = '';
    }

    // Generic Delete Confirmation Modal
    const confirmBtn = e.target.closest('[data-confirm-url]');
    if (confirmBtn) {
      e.preventDefault();
      const url = confirmBtn.dataset.confirmUrl;
      const msg = confirmBtn.dataset.confirmMsg || 'Are you sure you want to proceed?';
      const confirmForm = document.getElementById('confirmForm');
      const confirmMsgEl = document.getElementById('confirmMsg');
      const confirmModal = document.getElementById('confirmModal');

      if (confirmForm) confirmForm.action = url;
      if (confirmMsgEl) confirmMsgEl.textContent = msg;
      if (confirmModal) bootstrap.Modal.getOrCreateInstance(confirmModal).show();
    }

    // Edit Modal AJAX Population
    const editBtn = e.target.closest('[data-edit-url]');
    if (editBtn) {
      e.preventDefault();
      const url = editBtn.dataset.editUrl;
      const modalId = editBtn.dataset.modalId;
      const modal = document.querySelector(modalId);

      if (modal) {
        fetch(url)
          .then(resp => {
            if (!resp.ok) throw new Error('Not found');
            return resp.json();
          })
          .then(data => {
            Object.entries(data).forEach(([key, value]) => {
              const field = modal.querySelector(`[name="${key}"]`);
              if (field) field.value = value;
            });
            bootstrap.Modal.getOrCreateInstance(modal).show();
          })
          .catch(err => console.error('Edit modal fetch error:', err));
      }
    }

    // Result Modal Population
    const resultBtn = e.target.closest('[data-result-match-id]');
    if (resultBtn) {
      e.preventDefault();
      const url = resultBtn.dataset.resultUrl;
      const modal = document.getElementById('resultModal');
      const form = document.getElementById('resultForm');
      if (form) form.action = url;
      if (modal) bootstrap.Modal.getOrCreateInstance(modal).show();
    }
  });

  // Close sidebar on window resize if wide enough
  window.addEventListener('resize', function () {
    if (window.innerWidth >= 992) {
      const sidebar = document.getElementById('sidebar');
      const overlay = document.getElementById('sidebarOverlay');
      sidebar?.classList.remove('show');
      overlay?.classList.remove('show');
      document.body.style.overflow = '';
    }
  });

  /* ----------------------------------------------------------
     AUTO-DISMISS FLASH ALERTS (after 4s)
  ---------------------------------------------------------- */
  document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert?.close();
    }, 4500);
  });

  /* ----------------------------------------------------------
     SEARCH FORM: submit on typing with debounce (300ms)
  ---------------------------------------------------------- */
  document.querySelectorAll('.search-input-live').forEach(function (input) {
    let timer;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        input.closest('form').submit();
      }, 350);
    });
  });

  /* ----------------------------------------------------------
     FILTER SELECTS: submit immediately on change
  ---------------------------------------------------------- */
  document.querySelectorAll('.filter-select-auto').forEach(function (sel) {
    sel.addEventListener('change', function () {
      sel.closest('form').submit();
    });
  });

  /* ----------------------------------------------------------
     PASSWORD STRENGTH INDICATOR (register page)
  ---------------------------------------------------------- */
  const passInput = document.getElementById('password');
  const strengthBar = document.getElementById('strengthBar');
  if (passInput && strengthBar) {
    passInput.addEventListener('input', function () {
      const len = passInput.value.length;
      let pct = 0, color = '#ef4444';
      if (len >= 8)  { pct = 40; color = '#f0b429'; }
      if (len >= 12) { pct = 70; color = '#22854a'; }
      if (len >= 16) { pct = 100; color = '#1a6b3c'; }
      strengthBar.style.width = pct + '%';
      strengthBar.style.background = color;
    });
  }

  /* ----------------------------------------------------------
     SALARY FORMATTER: comma-separate numbers in salary field
  ---------------------------------------------------------- */
  document.querySelectorAll('input[name="salary"]').forEach(function (field) {
    field.addEventListener('blur', function () {
      const val = parseFloat(field.value);
      if (!isNaN(val)) field.value = val.toFixed(2);
    });
  });

  /* ----------------------------------------------------------
     ACTIVE NAV LINK HIGHLIGHT
  ---------------------------------------------------------- */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

});
