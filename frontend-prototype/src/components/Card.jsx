import { forwardRef } from 'react';
import { Brain, Zap } from 'lucide-react';

const Card = forwardRef(function Card({ arquetipo, horas, dias, libros, minutos, featuredBooks, mode = 'story', colorScheme = null }, ref) {
  const sourceBooks = (featuredBooks && featuredBooks.length > 0 ? featuredBooks : arquetipo.libros).slice(0, 3);
  const bookColors = ['#d4744f', '#2d7a6e', '#8b5a8f'];

  return (
    <article
      ref={ref}
      className={`share-card ${mode}`}
      style={colorScheme ? {
        background: colorScheme.bg,
        '--accent-color': colorScheme.accent,
      } : {}}
    >
      {/* Header */}
      <div className="card-header">
        <div className="card-brand">
          <div className="card-title-wrapper">
            <div className="card-icon-books">
              {['#ffd5bf', '#fff4e6', '#ffe8cc'].map((color, i) => (
                <div key={i} className="card-icon-book" style={{ background: color, height: `${10 + i * 3}px` }} />
              ))}
            </div>
            <h2 className="card-title">TIEMPO ROBADO</h2>
          </div>
          <p className="card-subtitle">criterio regalado</p>
        </div>
        <span className="card-handle">@anaisentrelineas</span>
      </div>

      {/* Main metric */}
      <div className="card-metric">
        <p className="metric-label">Recuperaré</p>
        <div className="metric-value">
          <span className="number">{horas}</span>
          <span className="unit">h/año</span>
        </div>
        <p className="metric-sub">{minutos ? `si dedico ${minutos} min/día a leer` : 'dedicando minutos a leer'}</p>
      </div>

      {/* Profile */}
      <div className="card-profile">
        <p className="profile-archetype">{arquetipo.nombre}</p>
        <p className="profile-meta">{dias} días de foco → {Math.round(libros)} libros/año</p>
      </div>

      {/* Benefits */}
      <div className="card-benefits">
        <div className="benefit">
          <Brain size={18} />
          <div>
            <p className="benefit-value">32%</p>
            <p className="benefit-text">mejor memoria</p>
          </div>
        </div>
        <div className="benefit">
          <Zap size={18} />
          <div>
            <p className="benefit-value">68%</p>
            <p className="benefit-text">más calma</p>
          </div>
        </div>
      </div>

      {/* Visual books shelf decoration */}
      <div className="card-books-visual">
        {['#d4744f', '#2d7a6e', '#8b5a8f', '#d4a052', '#5a7c8e', '#c76d5a', '#1f7a6f'].map((color, i) => (
          <div
            key={i}
            className="card-book-spine"
            style={{ background: color, height: `${28 + (i % 3) * 4}px` }}
          />
        ))}
      </div>

      {/* Books */}
      <div className="card-books">
        <p className="books-label">Lecturas para ti</p>
        <div className="books-list">
          {sourceBooks.map((book, idx) => (
            <div key={book.titulo} className="book-pill" style={{ background: bookColors[idx], borderColor: bookColors[idx] }}>
              <span className="book-number" style={{ background: 'rgba(255,255,255,0.25)' }}>{idx + 1}</span>
              <span className="book-name">{book.titulo}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Footer message */}
      <p className="card-footer">
        <svg className="footer-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="2" fill="currentColor" opacity="0.3"/>
          <circle cx="12" cy="4" r="2" fill="currentColor"/>
          <circle cx="12" cy="20" r="2" fill="currentColor" opacity="0.5"/>
          <line x1="12" y1="6" x2="12" y2="18" stroke="currentColor" strokeWidth="1" opacity="0.4"/>
        </svg>
        No era falta de voluntad. Hay algoritmos compitiendo. Pero leer es recuperar tu criterio.
      </p>
    </article>
  );
});

export default Card;