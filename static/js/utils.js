document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initMobileNav();
  initThemeMenu();
});

function initTheme() {
  const setTheme = (theme) => {
    const root = document.documentElement;
    const resolved =
      theme === 'auto'
        ? window.matchMedia('(prefers-color-scheme: dark)').matches
          ? 'dark'
          : 'light'
        : theme;

    root.classList.toggle('dark', resolved === 'dark');
    root.dataset.theme = theme;
    localStorage.setItem('theme', theme);

    document.querySelectorAll('[data-theme-value]').forEach((button) => {
      button.classList.toggle('dropdown-item-active', button.dataset.themeValue === theme);
    });
  };

  document.querySelectorAll('[data-theme-value]').forEach((button) => {
    button.addEventListener('click', () => setTheme(button.dataset.themeValue));
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if ((localStorage.getItem('theme') || 'auto') === 'auto') setTheme('auto');
  });

  setTheme(localStorage.getItem('theme') || 'auto');
}

function initMobileNav() {
  const toggle = document.getElementById('navbar-toggle');
  const menu = document.getElementById('navbar-menu');
  if (!toggle || !menu) return;

  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    menu.classList.toggle('hidden', expanded);
  });
}

function initThemeMenu() {
  const trigger = document.getElementById('theme-menu-trigger');
  const menu = document.getElementById('theme-menu');
  if (!trigger || !menu) return;

  trigger.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    const expanded = trigger.getAttribute('aria-expanded') === 'true';
    trigger.setAttribute('aria-expanded', String(!expanded));
    menu.classList.toggle('hidden', expanded);
  });

  document.addEventListener('click', (event) => {
    if (!trigger.contains(event.target) && !menu.contains(event.target)) {
      trigger.setAttribute('aria-expanded', 'false');
      menu.classList.add('hidden');
    }
  });
}
