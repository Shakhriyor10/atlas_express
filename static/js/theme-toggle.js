(function () {
  const STORAGE_KEY = 'atlas-theme';
  const toggles = document.querySelectorAll('[data-theme-toggle]');
  if (!toggles.length) {
    return;
  }

  const storage = {
    get() {
      try {
        return window.localStorage.getItem(STORAGE_KEY);
      } catch (error) {
        return null;
      }
    },
    set(value) {
      try {
        window.localStorage.setItem(STORAGE_KEY, value);
      } catch (error) {
        // Silently ignore when storage is not available (private mode, etc.)
      }
    },
  };

  const prefersDark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  const applyTheme = (theme) => {
    const normalizedTheme = theme === 'dark' ? 'dark' : 'light';
    document.body.classList.toggle('dark-theme', normalizedTheme === 'dark');
    document.documentElement.setAttribute('data-theme', normalizedTheme);
    toggles.forEach((toggle) => {
      toggle.dataset.themeState = normalizedTheme;
      toggle.setAttribute('aria-pressed', normalizedTheme === 'dark');
    });
  };

  const storedTheme = storage.get();
  const initialTheme = storedTheme || (prefersDark && prefersDark.matches ? 'dark' : 'light');
  applyTheme(initialTheme);

  const saveTheme = (theme) => {
    storage.set(theme);
  };

  toggles.forEach((toggle) => {
    toggle.addEventListener('click', () => {
      const isDark = document.body.classList.contains('dark-theme');
      const nextTheme = isDark ? 'light' : 'dark';
      applyTheme(nextTheme);
      saveTheme(nextTheme);
    });
  });

  if (prefersDark) {
    const mediaListener = (event) => {
      if (!storage.get()) {
        applyTheme(event.matches ? 'dark' : 'light');
      }
    };

    if (prefersDark.addEventListener) {
      prefersDark.addEventListener('change', mediaListener);
    } else if (prefersDark.addListener) {
      prefersDark.addListener(mediaListener);
    }
  }
})();