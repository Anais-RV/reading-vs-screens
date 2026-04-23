import { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const LETTERS = ['A', 'B', 'C', 'D'];

export default function Quiz({ answers, setAnswers, quizQuestions, onFinish, onBack }) {
  const currentIndex = answers.findIndex((ans) => ans === null);
  const safeIndex = currentIndex === -1 ? quizQuestions.length - 1 : currentIndex;
  const currentQuestion = quizQuestions[safeIndex];

  const progress = useMemo(() => {
    return Math.round((safeIndex / quizQuestions.length) * 100);
  }, [safeIndex, quizQuestions.length]);

  const chooseOption = (optionCode) => {
    const next = [...answers];
    next[safeIndex] = optionCode;
    setAnswers(next);

    if (safeIndex === quizQuestions.length - 1) {
      window.setTimeout(onFinish, 220);
    }
  };

  return (
    <section className="quiz-screen container">
      <div className="quiz-head">
        <button className="text-button" onClick={onBack}>Anterior</button>
        <span>Pregunta {safeIndex + 1} / {quizQuestions.length}</span>
      </div>
      <div className="progress-track">
        <div className="progress-bar" style={{ width: `${progress}%` }} />
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={currentQuestion.codigo}
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -14 }}
          transition={{ duration: 0.2 }}
          className="quiz-card"
        >
          <h3>{currentQuestion.texto}</h3>
          <p>{currentQuestion.reflexion} Elegir como lees tambien es elegir como piensas.</p>

          <div className="quiz-options">
            {currentQuestion.opciones.map((option, idx) => (
              <button
                key={option.codigo}
                className={`quiz-option ${answers[safeIndex] === option.codigo ? 'selected' : ''}`}
                onClick={() => chooseOption(option.codigo)}
              >
                <span className="option-letter">{LETTERS[idx]}</span>
                <span>{option.texto}</span>
              </button>
            ))}
          </div>
        </motion.div>
      </AnimatePresence>
    </section>
  );
}
