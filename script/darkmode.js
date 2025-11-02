(function(){
      const root = document.documentElement;
      const toggle = document.getElementById('themeToggle');
      const label = document.getElementById('themeLabel');
      const icon = document.getElementById('themeIcon');
      const storageKey = 'theme-preference'; // "light" | "dark" | null

      // Helper to set visuals
      function applyTheme(t){
        if(t === 'dark'){
          root.classList.add('dark');
          toggle.setAttribute('aria-pressed','true');
          label.textContent = 'Dark';
          icon.textContent = '🌙';
        } else {
          root.classList.remove('dark');
          toggle.setAttribute('aria-pressed','false');
          label.textContent = 'Light';
          icon.textContent = '☀️';
        }
      }

      // Read saved preference
      const saved = localStorage.getItem(storageKey);

      if(saved === 'dark' || saved === 'light'){
        applyTheme(saved);
      } else {
        // No saved pref — follow system preference
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(prefersDark ? 'dark' : 'light');
      }

      // Click handler — toggle and save
      toggle.addEventListener('click', () => {
        const isDark = root.classList.contains('dark');
        const next = isDark ? 'light' : 'dark';
        applyTheme(next);
        localStorage.setItem(storageKey, next);
      });

      // Optional: allow keyboard activation with Enter/Space
      toggle.addEventListener('keydown', (e) => {
        if(e.key === 'Enter' || e.key === ' '){
          e.preventDefault();
          toggle.click();
        }
      });

      // If user changes system theme and they haven't set a preference, update automatically
      window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        const savedNow = localStorage.getItem(storageKey);
        if(savedNow !== 'dark' && savedNow !== 'light'){
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    })();

/* project.html */
/* const toggle = document.getElementById('themeToggle');
    const icon = document.getElementById('themeIcon');

    toggle.addEventListener('click', () => {
      document.body.classList.toggle('dark');
      if (document.body.classList.contains('dark')) {
        icon.classList.replace('fa-moon', 'fa-sun');
      } else {
        icon.classList.replace('fa-sun', 'fa-moon');
      }
    }); */