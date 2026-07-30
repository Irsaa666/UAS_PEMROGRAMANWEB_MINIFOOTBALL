/* ============================================================
   Mini Football Manager - main.js
   Global JavaScript: sidebar toggle, modals, confirmations,
   flash auto-dismiss, AJAX helpers.
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ----------------------------------------------------------
     SIDEBAR TOGGLE (Mobile)
  ---------------------------------------------------------- */
  const sidebar        = document.getElementById('sidebar');
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const toggleBtn      = document.getElementById('sidebarToggle');

  function openSidebar() {
    sidebar?.classList.add('show');
    sidebarOverlay?.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    sidebar?.classList.remove('show');
    sidebarOverlay?.classList.remove('show');
    document.body.style.overflow = '';
  }

  toggleBtn?.addEventListener('click', function () {
    sidebar?.classList.contains('show') ? closeSidebar() : openSidebar();
  });

  sidebarOverlay?.addEventListener('click', closeSidebar);

  // Close sidebar on window resize if wide enough
  window.addEventListener('resize', function () {
    if (window.innerWidth >= 992) closeSidebar();
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
     GENERIC DELETE CONFIRMATION MODAL
     Usage: add data-confirm-url="/path" data-confirm-msg="Are you sure?"
     to a button, and include #confirmModal in layout.html
  ---------------------------------------------------------- */
  const confirmModal  = document.getElementById('confirmModal');
  const confirmForm   = document.getElementById('confirmForm');
  const confirmMsgEl  = document.getElementById('confirmMsg');

  document.querySelectorAll('[data-confirm-url]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const url = btn.dataset.confirmUrl;
      const msg = btn.dataset.confirmMsg || 'Are you sure you want to proceed?';
      if (confirmForm) confirmForm.action = url;
      if (confirmMsgEl) confirmMsgEl.textContent = msg;
      if (confirmModal) new bootstrap.Modal(confirmModal).show();
    });
  });

  /* ----------------------------------------------------------
     EDIT MODAL POPULATION via AJAX (fetch JSON from /*/get/<id>)
     Usage: add data-edit-url="/players/get/5" data-modal-id="#editPlayerModal"
     to a button. The returned JSON keys must match form field names.
  ---------------------------------------------------------- */
  document.querySelectorAll('[data-edit-url]').forEach(function (btn) {
    btn.addEventListener('click', async function () {
      const url     = btn.dataset.editUrl;
      const modalId = btn.dataset.modalId;
      const modal   = document.querySelector(modalId);
      if (!modal) return;

      try {
        const resp = await fetch(url);
        if (!resp.ok) throw new Error('Not found');
        const data = await resp.json();

        // Populate form fields whose name attribute matches JSON keys
        Object.entries(data).forEach(([key, value]) => {
          const field = modal.querySelector(`[name="${key}"]`);
          if (field) field.value = value;
        });

        new bootstrap.Modal(modal).show();
      } catch (err) {
        console.error('Edit modal fetch error:', err);
      }
    });
  });

  /* ----------------------------------------------------------
     RESULT MODAL POPULATION
     Usage: add data-result-match-id="5" data-result-url="/matches/result/5"
  ---------------------------------------------------------- */
  document.querySelectorAll('[data-result-match-id]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const matchId  = btn.dataset.resultMatchId;
      const url      = btn.dataset.resultUrl;
      const modal    = document.getElementById('resultModal');
      const form     = document.getElementById('resultForm');
      if (form) form.action = url;
      if (modal) new bootstrap.Modal(modal).show();
    });
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
