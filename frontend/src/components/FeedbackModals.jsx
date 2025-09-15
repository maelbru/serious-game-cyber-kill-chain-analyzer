/**
 * FEEDBACK MODALS COMPONENT
 * Gestisce tutti i modali di feedback del gioco
 */

import { GAME_STATES, FEEDBACK_TYPES } from '../utils/constants.js'

export function FeedbackModals({ 
  gameState, 
  feedback, 
  fetchNewLog, 
  isLoading,
  score,
  accuracy,
  level 
}) {

  // Non renderizzare nulla se non siamo in uno stato di feedback
  if (!feedback || (
    gameState !== GAME_STATES.PHASE_FEEDBACK && 
    gameState !== GAME_STATES.FINAL_FEEDBACK
  )) {
    return null
  }

  // ========================================
  // PHASE FEEDBACK (INCORRECT/TIMEOUT)
  // ========================================

  if (gameState === GAME_STATES.PHASE_FEEDBACK) {
    return (
      <div className="modal-overlay">
        <div className="feedback-modal">
          <div className={`feedback-icon ${
            feedback.type === FEEDBACK_TYPES.TIMEOUT ? 'warning' :
            feedback.type === FEEDBACK_TYPES.PHASE_CORRECT ? 'success' : 'error'
          }`}>
            {feedback.type === FEEDBACK_TYPES.TIMEOUT ? '⏰' :
             feedback.type === FEEDBACK_TYPES.PHASE_CORRECT ? '✓' : '✗'}
          </div>

          <h2 className="feedback-title">
            {feedback.type === FEEDBACK_TYPES.TIMEOUT ? 'Tempo Scaduto!' :
             feedback.type === FEEDBACK_TYPES.PHASE_CORRECT ? 'Risposta Corretta!' : 'Risposta Errata!'}
          </h2>

          {/* Messaggio specifico per timeout */}
          {feedback.type === FEEDBACK_TYPES.TIMEOUT && (
            <div className="timeout-message">
              <p>{feedback.message}</p>
            </div>
          )}

          {/* Mostra risposta corretta solo se NON è timeout E c'è una risposta corretta */}
          {feedback.correct_phase && feedback.type !== FEEDBACK_TYPES.TIMEOUT && (
            <div className="correct-answer">
              <h3>La fase corretta era:</h3>
              <div className="phase-card highlighted">
                <span className="phase-icon">{feedback.phase_info?.icon}</span>
                <span className="phase-name">{feedback.phase_info?.name}</span>
                <p className="phase-description">{feedback.phase_info?.description}</p>
              </div>
            </div>
          )}

          {feedback.explanation && (
            <div className="explanation-box">
              <h4>📚 {feedback.type === FEEDBACK_TYPES.TIMEOUT ? 'Suggerimento:' : 'Spiegazione:'}</h4>
              <p>{feedback.explanation}</p>
            </div>
          )}

          {feedback.indicators && feedback.indicators.length > 0 && feedback.type !== FEEDBACK_TYPES.TIMEOUT && (
            <div className="indicators-box">
              <h4>🔍 Indicatori Chiave:</h4>
              <ul>
                {feedback.indicators.map((indicator, idx) => (
                  <li key={idx}>{indicator}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Consigli specifici per timeout */}
          {feedback.type === FEEDBACK_TYPES.TIMEOUT && (
            <div className="timeout-tips">
              <h4>💡 Suggerimenti per il prossimo round:</h4>
              <ul>
                <li>Leggi rapidamente il log cercando parole chiave</li>
                <li>Identifica la fonte (Rete, Email, Endpoint, ecc.)</li>
                <li>Cerca indicatori di azione (scansione, query, iniezione, ecc.)</li>
                <li>Non pensarci troppo - fidati del primo istinto</li>
              </ul>
            </div>
          )}

          <button
            className="btn-primary"
            onClick={fetchNewLog}
            disabled={isLoading}
          >
            {isLoading ? 'Caricamento...' : 'Prossimo Log →'}
          </button>
        </div>
      </div>
    )
  }

  // ========================================
  // FINAL FEEDBACK (MITIGATION RESULT)
  // ========================================

  if (gameState === GAME_STATES.FINAL_FEEDBACK) {
    return (
      <div className="modal-overlay">
        <div className="feedback-modal final">
          <div className={`feedback-icon ${feedback.is_correct ? 'success' : 'warning'}`}>
            {feedback.is_correct ? '🏆' : '💡'}
          </div>

          <h2 className="feedback-title">
            {feedback.is_correct ? 'Eccellente!' : 'Buon Tentativo!'}
          </h2>

          <div className="points-earned">
            <span className="points-label">Punti Guadagnati:</span>
            <span className="points-value">+{feedback.points}</span>
          </div>

          {feedback.selected_effectiveness && (
            <div className="effectiveness-feedback">
              <p>La tua scelta aveva un'efficacia: <strong>{feedback.selected_effectiveness}</strong></p>
              {!feedback.is_correct && feedback.best_mitigation && (
                <div className="best-strategy">
                  <h4>Strategia Ottimale:</h4>
                  <div className="mitigation-card optimal">
                    <span className="mitigation-icon">{feedback.best_mitigation.icon}</span>
                    <h3>{feedback.best_mitigation.name}</h3>
                    <p>{feedback.best_mitigation.description}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="progress-summary">
            <h4>I Tuoi Progressi:</h4>
            <div className="progress-stats">
              <div className="progress-item">
                <span>Punteggio Totale</span>
                <span>{score}</span>
              </div>
              <div className="progress-item">
                <span>Precisione</span>
                <span>{accuracy}%</span>
              </div>
              <div className="progress-item">
                <span>Livello</span>
                <span>{level}</span>
              </div>
            </div>
          </div>

          <button
            className="btn-primary"
            onClick={fetchNewLog}
            disabled={isLoading}
          >
            {isLoading ? 'Caricamento...' : 'Continua →'}
          </button>
        </div>
      </div>
    )
  }

  return null
}