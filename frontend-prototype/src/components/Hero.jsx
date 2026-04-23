import { motion } from 'framer-motion';
import HeroIllustration from './HeroIllustration';

export default function Hero({ onStart }) {
  return (
    <section className="hero container">
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="hero-copy"
      >
        <p className="hero-kicker">Lectura = Poder</p>
        <h1>
          Cada minuto scrolleando
          <span className="hero-emphasis"> es tiempo que no lees</span>
        </h1>
        <p className="hero-subtitle">
          El scroll no es inocente: está diseñado para retenerte.
          Leer es una forma de recuperar foco, criterio y libertad.
        </p>
        <button className="cta-button" onClick={onStart}>
          Empezar a reclamar mi tiempo
        </button>
      </motion.div>

      <motion.aside
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.15, duration: 0.45 }}
        className="hero-media"
      >
        <div className="book-photo">
          <HeroIllustration />
        </div>
        <p className="media-label">SLOW DATA MOVEMENT</p>
        <p className="media-quote">
          No es falta de disciplina: hay una industria compitiendo por tu atención.
          Recámala de vuelta, página a página.
        </p>
      </motion.aside>
    </section>
  );
}
