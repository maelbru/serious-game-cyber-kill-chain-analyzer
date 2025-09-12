/**
 * WELCOME SCREEN COMPONENT
 * Gestisce schermata di benvenuto e tutorial
 */

import { KILL_CHAIN_PHASES, GAME_STATES } from '../utils/constants.js'

export function WelcomeScreen({ 
  gameState,
  setGameState, 
  fetchNewLog, 
  isLoading, 
  isBackendAvailable 
}) {

  // ========================================
  // TUTORIAL SCREEN
  // ========================================

  if (gameState === GAME_STATES.TUTORIAL) {
    return (
      <div className="tutorial-screen">
        <div className="tutorial-content">
          <div className="tutorial-header">
            <h1>📖 Come Giocare</h1>
            <p>Impara a identificare e fermare gli attacchi informatici!</p>
          </div>

          <div className="tutorial-steps">
            <div className="tutorial-step">
              <span className="step-number">1</span>
              <div className="step-content">
                <h3>📋 Analizza il Log</h3>
                <p>Ogni round ti verrà presentato un log di sicurezza reale. Leggilo attentamente per identificare indicatori di attacco.</p>
              </div>
            </div>

            <div className="tutorial-step">
              <span className="step-number">2</span>
              <div className="step-content">
                <h3>🎯 Identifica la Fase</h3>
                <p>Basandoti sugli indicatori nel log, determina in quale delle 7 fasi della Cyber Kill Chain si trova l'attacco.</p>
              </div>
            </div>

            <div className="tutorial-step">
              <span className="step-number">3</span>
              <div className="step-content">
                <h3>🛡️ Scegli la Mitigazione</h3>
                <p>Se identifichi correttamente la fase, dovrai scegliere la strategia di mitigazione più efficace per interrompere l'attacco.</p>
              </div>
            </div>

            <div className="tutorial-step">
              <span className="step-number">4</span>
              <div className="step-content">
                <h3>⏱️ Tempo e Punti</h3>
                <p>Più velocemente rispondi correttamente, più punti guadagni! Il timer si adatta alla tua bravura.</p>
              </div>
            </div>
          </div>

          <button 
            className="btn-start-game" 
            onClick={() => setGameState(GAME_STATES.WELCOME)}
          >
            Capito! Iniziamo 🚀
          </button>
        </div>
      </div>
    )
  }

  // ========================================
  // WELCOME SCREEN
  // ========================================

  return (
    <div className="welcome-screen">
      <div className="welcome-content">
        <div className="logo-container">
          <div className="logo-circle">
            <span className="logo-icon">🛡️</span>
          </div>
          <div className="logo-text">Cyber Kill Chain</div>
          <div className="logo-subtitle">Analyzer</div>
        </div>

        <p className="welcome-description">
          Impara a identificare e interrompere gli attacchi informatici
          analizzando log di sicurezza reali attraverso le 7 fasi della Cyber Kill Chain
        </p>

        {!isBackendAvailable && (
          <div className="offline-notice">
            <span className="offline-icon">📡</span>
            <span>Modalità Offline Attiva - Funzionalità limitate</span>
          </div>
        )}

        <div className="kill-chain-preview">
          {KILL_CHAIN_PHASES.map((phase, index) => (
            <div key={phase.id} className="preview-phase">
              <span className="phase-number">{index + 1}</span>
              <span className="phase-icon">{phase.icon}</span>
              <span className="phase-name">{phase.name}</span>
            </div>
          ))}
        </div>

        <div className="welcome-buttons">
          <button
            className="btn-primary"
            onClick={fetchNewLog}
            disabled={isLoading}
          >
            {isLoading ? '⏳ Caricamento...' : '🎮 Inizia a Giocare'}
          </button>
          <button 
            className="btn-secondary" 
            onClick={() => setGameState(GAME_STATES.TUTORIAL)}
          >
            📖 Tutorial
          </button>
        </div>
      </div>
    </div>
  )
}