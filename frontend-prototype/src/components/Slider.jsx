import { useMemo } from 'react';
import { motion } from 'framer-motion';
import data from '../data/reading-power.json';

export default function Slider({ value, onChange, onNext }) {
  const result = useMemo(() => {
    return data.tabla_conversion_slider.find((row) => row.minutos_reclamados === value);
  }, [value]);

  const bookCount = result ? Math.min(Math.ceil(result.libros_aprox / 10), 5) : 0;

  return (
    <section className="slider-screen container">
      <p className="section-kicker">Tu auditoría de atención</p>
      <h2>Desliza: ¿cuánto tiempo quieres recuperar?</h2>

      <div className="slider-card">
        <div className="slider-header">
          <label htmlFor="minutes">Minutos diarios que le quitas al algoritmo</label>
          <div className="minutes-readout">{value} min</div>
        </div>

        <input
          id="minutes"
          type="range"
          min="0"
          max="180"
          step="15"
          value={value}
          onChange={(event) => onChange(Number(event.target.value))}
          className="slider"
        />

        <div className="slider-scale">
          <span>0</span>
          <span>90</span>
          <span>180 min</span>
        </div>

        {result && (
          <motion.div
            className="slider-results"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {/* Top metrics row */}
            <div className="metrics-row">
              <div className="metric-item">
                <p className="label">Tiempo recuperado (anual)</p>
                <p className="value">{result.horas_anuales} h</p>
              </div>
              <div className="metric-item">
                <p className="label">Días de foco (anuales)</p>
                <p className="value">{result.dias_completos}</p>
              </div>
            </div>

            {/* Visual: Screen waste vs Books gain */}
            <div className="visual-contrast">
              {/* Screen time wasted */}
              <div className="screen-section">
                <p className="contrast-label">Pantalla robada</p>
                <svg className="phone-visual" viewBox="0 0 60 100" xmlns="http://www.w3.org/2000/svg">
                  {/* Phone frame */}
                  <rect x="5" y="5" width="50" height="90" rx="4" fill="none" stroke="#9e9e9e" strokeWidth="2"/>
                  {/* Phone notch */}
                  <rect x="18" y="5" width="24" height="6" rx="2" fill="#9e9e9e"/>
                  {/* Screen fill */}
                  <defs>
                    <clipPath id="screenClip">
                      <rect x="7" y="13" width="46" height="76" rx="2"/>
                    </clipPath>
                  </defs>
                  <rect x="7" y="13" width="46" height={`${76 * Math.min((420 / 180) * value, 100) / 100}`} fill="#ff6e60" clipPath="url(#screenClip)"/>
                  {/* Screen background */}
                  <rect x="7" y="13" width="46" height="76" rx="2" fill="none" stroke="#d9d9d9" strokeWidth="0.5" opacity="0.5"/>
                </svg>
                <p className="contrast-value">{Math.round((420 / 180) * value)} min</p>
              </div>

              {/* Arrow */}
              <div className="contrast-arrow">→</div>

              {/* Books gained */}
              <div className="books-section">
                <p className="contrast-label">Libros ganados</p>
                <div className="books-visual">
                  {[...Array(5)].map((_, i) => {
                    const colors = ['#d4744f', '#2d7a6e', '#8b5a8f', '#d4a052', '#5a7c8e'];
                    return (
                      <div
                        key={i}
                        className={`book-spine ${i < bookCount ? 'active' : ''}`}
                        style={{
                          background: colors[i % colors.length],
                          animationDelay: `${i * 0.1}s`,
                        }}
                      />
                    );
                  })}
                </div>
                <p className="contrast-value">~{result.libros_aprox} libros/año</p>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      <button onClick={onNext} className="cta-button">
        Siguiente: descubrir mi perfil lector
      </button>
    </section>
  );
}
