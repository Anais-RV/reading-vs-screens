import { useMemo, useState } from 'react';
import Hero from './components/Hero';
import Slider from './components/Slider';
import Quiz from './components/Quiz';
import Result from './components/Result';
import data from './data/reading-power.json';

const PRIORITY = [
  'lectora-politica',
  'escapista-politica',
  'exploradora-empatica',
  'archivista-de-lo-real',
  'aventurera-reflexiva',
];

function computeBySlider(minutes) {
  const row = data.tabla_conversion_slider.find(
    (item) => item.minutos_reclamados === minutes
  );
  if (row) {
    return {
      horas: row.horas_anuales,
      dias: row.dias_completos,
      libros: row.libros_aprox,
    };
  }

  const horas = Number(((minutes * 365) / 60).toFixed(1));
  const dias = Number((horas / 24).toFixed(1));
  const libros = Number(
    (
      (minutes * 365 * data.parametros_base.minutes_to_pages) /
      data.parametros_base.avg_pages_per_book
    ).toFixed(1)
  );
  return { horas, dias, libros };
}

function resolveArchetype(answers) {
  const weights = data.quiz_logic.weights;
  const scores = {};

  data.arquetipos.forEach((archetype) => {
    scores[archetype.id] = 0;
  });

  answers.forEach((code, index) => {
    const section = `P${index + 1}`;
    const source = weights[section]?.[code] || {};
    Object.entries(source).forEach(([archetypeId, value]) => {
      scores[archetypeId] += value;
    });
  });

  const winner = Object.keys(scores).sort((a, b) => {
    if (scores[b] !== scores[a]) return scores[b] - scores[a];
    return PRIORITY.indexOf(a) - PRIORITY.indexOf(b);
  })[0];

  return data.arquetipos.find((item) => item.id === winner);
}

function App() {
  const [step, setStep] = useState('hero');
  const [sliderValue, setSliderValue] = useState(60);
  const [answers, setAnswers] = useState([null, null, null]);

  const result = useMemo(() => {
    if (answers.some((answer) => answer === null)) return null;
    const arquetipo = resolveArchetype(answers);
    if (!arquetipo) return null;
    return {
      arquetipo,
      ...computeBySlider(sliderValue),
    };
  }, [answers, sliderValue]);

  const restartFlow = () => {
    setStep('hero');
    setSliderValue(60);
    setAnswers([null, null, null]);
  };

  return (
    <main className="app-shell">
      <header className="top-nav">
        <button className="brand-home" onClick={restartFlow}>
          <h1 className="brand">TIEMPO ROBADO</h1>
          <span className="brand-subtitle">criterio regalado</span>
        </button>
        <a href="https://instagram.com/anaisentrelineas" target="_blank" rel="noopener noreferrer" className="brand-pill">
          @anaisentrelineas
        </a>
      </header>

      {step === 'hero' && <Hero onStart={() => setStep('slider')} />}

      {step === 'slider' && (
        <Slider
          value={sliderValue}
          onChange={setSliderValue}
          onNext={() => setStep('quiz')}
        />
      )}

      {step === 'quiz' && (
        <Quiz
          answers={answers}
          setAnswers={setAnswers}
          quizQuestions={data.quiz_logic.preguntas}
          onBack={() => setStep('slider')}
          onFinish={() => setStep('result')}
        />
      )}

      {step === 'result' && result && (
        <Result
          result={result}
          sliderValue={sliderValue}
          onRestart={restartFlow}
          onBackQuiz={() => setStep('quiz')}
        />
      )}

      <footer className="site-footer">
        <p className="footer-brand">TIEMPO ROBADO • CRITERIO REGALADO</p>
        <p>Leer es recuperar tu tiempo, foco y criterio. Una respuesta política ante algoritmos que compiten por tu atención.</p>
      </footer>
    </main>
  );
}

export default App;
