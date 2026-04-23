import { useEffect, useState } from 'react';

const THEMES = {
  default: { name: 'Teal', teal: '#0b6b67', coral: '#ff6e60' },
  purple: { name: 'Púrpura', teal: '#6b3ba0', coral: '#ff6b9d' },
  blue: { name: 'Azul', teal: '#1e5a96', coral: '#ff8c42' },
  forest: { name: 'Bosque', teal: '#2d5a3d', coral: '#e8764f' },
  ocean: { name: 'Océano', teal: '#0d5a7a', coral: '#f4a261' },
};

export default function ThemeSelector() {
  const [theme, setTheme] = useState('default');
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('readingTheme') || 'default';
    setTheme(saved);
    applyTheme(saved);
  }, []);

  const applyTheme = (themeName) => {
    const themeData = THEMES[themeName];
    document.documentElement.style.setProperty('--teal', themeData.teal);
    document.documentElement.style.setProperty('--teal-dark', adjustColor(themeData.teal, -20));
    document.documentElement.style.setProperty('--coral', themeData.coral);
    localStorage.setItem('readingTheme', themeName);
  };

  const handleThemeChange = (themeName) => {
    setTheme(themeName);
    applyTheme(themeName);
    setOpen(false);
  };

  const adjustColor = (color, percent) => {
    const num = parseInt(color.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = (num >> 8 & 0x00FF) + amt;
    const B = (num & 0x0000FF) + amt;
    return `#${(0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 + (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 + (B < 255 ? B < 1 ? 0 : B : 255)).toString(16).slice(1)}`;
  };

  return (
    <div className="theme-selector">
      <button
        className="theme-button"
        onClick={() => setOpen(!open)}
        title="Personaliza los colores"
      >
        🎨
      </button>

      {open && (
        <div className="theme-menu">
          <p className="theme-title">Personaliza tu tema</p>
          <div className="theme-options">
            {Object.entries(THEMES).map(([key, data]) => (
              <button
                key={key}
                className={`theme-option ${theme === key ? 'active' : ''}`}
                onClick={() => handleThemeChange(key)}
                style={{
                  background: `linear-gradient(135deg, ${data.teal}, ${data.coral})`,
                }}
                title={data.name}
              >
                {theme === key && '✓'}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
