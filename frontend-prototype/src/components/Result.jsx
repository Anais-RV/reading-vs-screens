import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import html2canvas from 'html2canvas';
import { motion } from 'framer-motion';
import Card from './Card';
import ComparisonChart from './ComparisonChart';

// Queries en español para Google Books (langRestrict=es devuelve ediciones en castellano)
const QUERIES_BY_ARCHETYPE = {
  'escapista-politica': ['distopia ficcion', 'ciencia ficcion politica', 'ficcion especulativa'],
  'exploradora-empatica': ['novela contemporanea empatia', 'ficcion social', 'literatura contemporanea'],
  'lectora-politica': ['politica feminismo ensayo', 'critica social', 'teoria feminista'],
  'aventurera-reflexiva': ['aventura viajes', 'cronica viaje', 'biografia exploradores'],
  'archivista-de-lo-real': ['historia contemporanea', 'periodismo narrativo', 'ensayo historia'],
};

const GENRE_BY_QUERY = {
  'distopia ficcion': 'Distopía',
  'ciencia ficcion politica': 'Ficción política',
  'ficcion especulativa': 'Ciencia ficción',
  'novela contemporanea empatia': 'Ficción contemporánea',
  'ficcion social': 'Ficción social',
  'literatura contemporanea': 'Literatura contemporánea',
  'politica feminismo ensayo': 'Ensayo político',
  'critica social': 'Crítica social',
  'teoria feminista': 'Feminismo',
  'aventura viajes': 'Aventura',
  'cronica viaje': 'Crónica de viaje',
  'biografia exploradores': 'Biografía',
  'historia contemporanea': 'Historia',
  'periodismo narrativo': 'Periodismo',
  'ensayo historia': 'Ensayo histórico',
};

// Normaliza un volumen de Google Books API
function normalizeVolume(item, query) {
  const info = item.volumeInfo || {};
  const paginas = info.pageCount || null;
  const thumb = info.imageLinks?.thumbnail || info.imageLinks?.smallThumbnail || null;
  // Google Books devuelve URLs http — forzamos https
  const cover_url = thumb ? thumb.replace('http://', 'https://') : null;
  return {
    titulo: info.title || 'Sin título',
    autor: Array.isArray(info.authors) ? info.authors[0] : 'Autor desconocido',
    paginas,
    genero: GENRE_BY_QUERY[query] || 'Ficción',
    horas_estimadas: paginas ? Number((paginas / 40).toFixed(1)) : null,
    por_que_aqui: 'Recomendación dinámica basada en tu perfil lector.',
    cover_url,
  };
}

function uniqueByTitle(books) {
  const seen = new Set();
  return books.filter((b) => {
    if (seen.has(b.titulo)) return false;
    seen.add(b.titulo);
    return true;
  });
}

function BookMeta({ book }) {
  const parts = [
    book.paginas ? `${book.paginas} págs` : null,
    book.genero || null,
    book.horas_estimadas ? `${book.horas_estimadas} h` : null,
  ].filter(Boolean);
  if (parts.length === 0) return null;
  return <p className="meta">{parts.join(' · ')}</p>;
}

export default function Result({ result, sliderValue, onRestart, onBackQuiz }) {
  const cardRef = useRef(null);
  const [cardMode, setCardMode] = useState('story');
  const [cardColor, setCardColor] = useState('default');
  const [showMoreData, setShowMoreData] = useState(false);
  const [apiBooks, setApiBooks] = useState([]);
  const [booksLoading, setBooksLoading] = useState(false);
  const [rotationSeed, setRotationSeed] = useState(0);

  const cardColors = {
    default: { bg: 'linear-gradient(135deg, #1a8c7a 0%, #0f6b61 50%, #0a5a54 100%)', accent: '#ffd5bf' },
    purple: { bg: 'linear-gradient(135deg, #7d5ba3 0%, #5c3e85 50%, #6b4d94 100%)', accent: '#ffc4f0' },
    blue: { bg: 'linear-gradient(135deg, #2167b1 0%, #1a4a8f 50%, #1f5fa3 100%)', accent: '#ffc857' },
    forest: { bg: 'linear-gradient(135deg, #3d6e4f 0%, #2a4e39 50%, #32594a 100%)', accent: '#f0ad6b' },
  };

  const fallbackBooks = useMemo(
    () => result.arquetipo.libros.slice(0, 5),
    [result.arquetipo.libros]
  );
  const topBooks = apiBooks.length > 0 ? apiBooks : fallbackBooks;

  const fetchBooksByArchetype = useCallback(async () => {
    const queries = QUERIES_BY_ARCHETYPE[result.arquetipo.id];
    if (!queries) return;
    setBooksLoading(true);
    try {
      const offset = rotationSeed % queries.length;
      const picks = [...queries.slice(offset), ...queries.slice(0, offset)].slice(0, 2);
      const startIndex = (rotationSeed * 5) % 15; // rota dentro de los resultados
      const results = await Promise.all(
        picks.map((q) =>
          fetch(
            `https://www.googleapis.com/books/v1/volumes?q=${encodeURIComponent(q)}&langRestrict=es&maxResults=20&startIndex=${startIndex}&orderBy=relevance&printType=books`
          )
            .then((r) => r.json())
            .then((d) => (d.items || []).map((item) => normalizeVolume(item, q)))
        )
      );
      const all = uniqueByTitle(results.flat());
      setApiBooks(all.slice(0, 5));
    } catch {
      setApiBooks([]);
    } finally {
      setBooksLoading(false);
    }
  }, [result.arquetipo.id, rotationSeed]);

  useEffect(() => {
    fetchBooksByArchetype();
  }, [fetchBooksByArchetype]);

  const downloadCard = async () => {
    const canvas = await html2canvas(cardRef.current, {
      backgroundColor: null,
      scale: 2,
      useCORS: true,
    });
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = `lectura-poder-${result.arquetipo.id}-${cardMode}.png`;
    link.click();
  };

  return (
    <section className="result-screen container">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
        <p className="section-kicker">Tu perfil</p>
        <h2>{result.arquetipo.nombre}</h2>
        <p className="result-description">{result.arquetipo.descripcion}</p>
        <p className="result-motivation">{result.arquetipo.motivacion_principal}</p>

        <div className="result-metrics">
          <article>
            <p>{result.horas}</p>
            <span>horas de lectura recuperadas</span>
          </article>
          <article>
            <p>{result.dias}</p>
            <span>días completos de foco</span>
          </article>
          <article>
            <p>~{result.libros}</p>
            <span>libros aproximados</span>
          </article>
        </div>

        <ComparisonChart screenTime={420} readingTime={18} />

        <div className="books-list">
          <div className="books-header">
            <h3>Lecturas recomendadas para ti</h3>
            <button
              type="button"
              className="rotation-button"
              onClick={() => setRotationSeed((s) => s + 1)}
              disabled={booksLoading}
            >
              {booksLoading ? 'Buscando…' : '↻ Rotar sugerencias'}
            </button>
          </div>
          {booksLoading && <p className="books-source">Cargando desde Google Books…</p>}
          {!booksLoading && apiBooks.length > 0 && (
            <p className="books-source">Sugerencias dinámicas · Google Books</p>
          )}
          {topBooks.map((book, idx) => (
            <article key={book.titulo} className="book-item">
              {book.cover_url
                ? <img className="book-cover image" src={book.cover_url} alt={`Portada de ${book.titulo}`} width={72} height={104} />
                : <div className="book-cover" style={{ '--h': 24 + idx * 46 }} aria-hidden="true" />}
              <div className="book-copy">
                <h4>{book.titulo}</h4>
                <p className="author">{book.autor}</p>
                <BookMeta book={book} />
                <p className="why">{book.por_que_aqui}</p>
              </div>
            </article>
          ))}
        </div>

        <div className="card-mode-switch" role="tablist" aria-label="Formato de card">
          <button
            type="button"
            className={cardMode === 'story' ? 'active' : ''}
            onClick={() => setCardMode('story')}
          >
            Ver card en Story
          </button>
          <button
            type="button"
            className={cardMode === 'feed' ? 'active' : ''}
            onClick={() => setCardMode('feed')}
          >
            Ver card en Feed
          </button>
        </div>

        <div className="card-color-selector">
          <p className="color-label">Personaliza el color de tu card:</p>
          <div className="color-options">
            {Object.entries(cardColors).map(([key, colors]) => (
              <button
                key={key}
                className={`color-option ${cardColor === key ? 'active' : ''}`}
                style={{ background: colors.bg }}
                onClick={() => setCardColor(key)}
                title={key}
              />
            ))}
          </div>
        </div>

        <Card
          ref={cardRef}
          arquetipo={result.arquetipo}
          horas={result.horas}
          dias={result.dias}
          libros={result.libros}
          minutos={sliderValue}
          featuredBooks={topBooks}
          mode={cardMode}
          colorScheme={cardColors[cardColor]}
        />

        <button className="cta-button" onClick={downloadCard}>
          {cardMode === 'story'
            ? 'Descargar Story listo para Instagram'
            : 'Descargar Feed listo para Instagram'}
        </button>
        <button className="secondary-button" onClick={onBackQuiz}>Volver al quiz</button>
        <button className="secondary-button" onClick={onRestart}>Empezar de nuevo</button>
      </motion.div>
    </section>
  );
}
