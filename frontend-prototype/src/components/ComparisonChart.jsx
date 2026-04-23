export default function ComparisonChart({ screenTime = 420, readingTime = 18 }) {
  const total = screenTime + readingTime;
  const screenPercent = (screenTime / total) * 100;
  const readPercent = (readingTime / total) * 100;

  return (
    <div className="comparison-chart">
      <p className="chart-header">Frente a la media en España</p>
      <div className="chart-row">
        <div className="chart-label">
          <span>📱 Pantalla</span>
          <span className="value">{screenTime} min/día</span>
        </div>
        <div className="chart-bar-container">
          <div
            className="chart-bar screen"
            style={{ width: `${Math.min(screenPercent, 95)}%` }}
          />
        </div>
      </div>

      <div className="chart-row">
        <div className="chart-label">
          <span>📖 Lectura</span>
          <span className="value">{readingTime} min/día</span>
        </div>
        <div className="chart-bar-container">
          <div
            className="chart-bar read"
            style={{ width: `${readPercent}%` }}
          />
        </div>
      </div>

      <p className="chart-note">Fuente: Reuters Institute 2024</p>
    </div>
  );
}
