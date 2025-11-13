(function () {
  const root = document.documentElement;
  const body = document.body;
  const toggle = document.getElementById('theme-toggle');
  const stored = localStorage.getItem('pg-theme') || 'light';

  const applyTheme = (theme) => {
    root.setAttribute('data-theme', theme);
    body.setAttribute('data-theme', theme);
    localStorage.setItem('pg-theme', theme);
    if (toggle) {
      toggle.classList.toggle('is-dark', theme === 'dark');
    }
  };

  applyTheme(stored);

  if (toggle) {
    toggle.addEventListener('click', () => {
      const nextTheme = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      applyTheme(nextTheme);
    });
  }

  const swatches = document.querySelectorAll('[data-card-theme-trigger]');
  swatches.forEach((btn) => {
    btn.addEventListener('click', () => {
      const theme = btn.dataset.cardThemeTrigger;
      const targetId = btn.dataset.target;
      const card = document.getElementById(targetId);
      if (!card) return;
      card.dataset.theme = theme;
      const container = btn.closest('.swatch-row');
      if (!container) return;
      container.querySelectorAll('button').forEach((el) => {
        el.classList.toggle('active', el === btn);
      });
    });
  });

  document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-role-link]');
    if (!target) return;
    const group = target.dataset.roleGroup;
    const selector = group ? `[data-role-link][data-role-group=\"${group}\"]` : '[data-role-link]';
    document.querySelectorAll(selector).forEach((link) => link.classList.remove('active'));
    target.classList.add('active');
  });
})();
