/**
 * GAME SCREEN COMPONENT
 * Schermata principale di gioco e selezione mitigazione
 */

import { KILL_CHAIN_PHASES, DIFFICULTY_CONFIG, GAME_STATES } from '../utils/constants.js'

export function GameScreen({
  // Game State
  gameState,
  difficulty,
  isBackendAvailable,
  
  // Player Stats
  score,
  streak,
  level,
  accuracy,
  
  // Current Round
  currentLog,
  timeRemaining,
  selectedPhase,
  setSelectedPhase,
  selectedMitigation,
  setSelectedMitigation,
  mitigationStrategies,
  
  // UI State
  isLoading,
  
  // Actions
  validatePhase,
  validateMitigation
}) {

  // ========================================
  // MITIGATION SELECTION SCREEN
  // ========================================

  if (gameState === GAME_STATES.MITIGATION) {
    return (
      <div className="game-container">
        <header className="game-header">
          <div className="header-stats">
            <div className="stat-item">
              <span className="stat-label">Score</span>
              <span className="stat-value">{score}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Streak</span>
              <span className="stat-value">{streak}🔥</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Level</span>
              <span className="stat-value">{level}</span>
            </div>
          </div>
        </header>

        <div className="mitigation-container">
          <div className="success-message">
            <span className="success-icon">✓</span>
            <h2>Ottimo! Hai identificato correttamente la fase.</h2>
            <p>Ora seleziona la strategia di mitigazione più efficace per interrompere la Kill Chain:</p>
          </div>

          <div className="mitigation-grid">
            {mitigationStrategies.map(strategy => (
              <div
                key={strategy.id}
                className={`mitigation-card ${selectedMitigation === strategy.id ? 'selected' : ''}`}
                onClick={() => setSelectedMitigation(strategy.id)}
              >
                <div className="mitigation-header">
                  <span className="mitigation-icon">{strategy.icon}</span>
                  <span className={`effectiveness-badge ${strategy.effectiveness.toLowerCase().replace(' ', '-')}`}>
                    {strategy.effectiveness}
                  </span>
                </div>
                <h3>{strategy.name}</h3>
                <p>{strategy.description}</p>
              </div>
            ))}
          </div>

          <button
            className="btn-submit"
            onClick={validateMitigation}
            disabled={!selectedMitigation || isLoading}
          >
            {isLoading ? 'Validazione...' : 'Conferma Mitigazione'}
          </button>
        </div>
      </div>
    )
  }

  // ========================================
  // MAIN GAME SCREEN
  // ========================================

  return (
    <div className="game-container">
      <header className="game-header">
        <div className="logo-small">
          <span>🛡️</span>
          <span>CKC Analyzer</span>
        </div>

        <div className="header-stats">
          <div className="stat-item">
            <span className="stat-label">Score</span>
            <span className="stat-value">{score}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Streak</span>
            <span className="stat-value">{streak}🔥</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Accuracy</span>
            <span className="stat-value">{accuracy}%</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Level</span>
            <span className="stat-value">{level}</span>
          </div>
        </div>

        <div className={`difficulty-badge ${difficulty}`}>
          {difficulty.toUpperCase()}
          {!isBackendAvailable && <span className="offline-indicator">📡</span>}
        </div>
      </header>

      <div className="game-content">
        {/* ========================================
            LOG SECTION
            ======================================== */}
        <div className="log-section">
          <div className="section-header">
            <h2>📋 Analisi dei log di sicurezza</h2>
            <div className={`timer ${
              timeRemaining <= 15 ? 'critical' : 
              timeRemaining <= 30 ? 'warning' : ''
            }`}>
              ⏱️ {timeRemaining}s
            </div>
          </div>

          {currentLog && (
            <div className="log-card">
              <div className="log-header">
                <span className={`severity-badge ${currentLog.severity?.toLowerCase()}`}>
                  {currentLog.severity}
                </span>
                <span className="log-source">{currentLog.source}</span>
                <span className="log-time">{currentLog.timestamp}</span>
              </div>

              <div className="log-content">
                <pre>{currentLog.raw}</pre>
              </div>

              {currentLog.metadata && Object.keys(currentLog.metadata).length > 0 && (
                <div className="log-metadata">
                  <h4>Metadata:</h4>
                  <div className="metadata-grid">
                    {Object.entries(currentLog.metadata).map(([key, value]) => (
                      <div key={key} className="metadata-item">
                        <span className="meta-key">{key}:</span>
                        <span className="meta-value">{String(value)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {isLoading && (
            <div className="loading-indicator">
              <span className="loading-spinner">⏳</span>
              <span>Caricamento log...</span>
            </div>
          )}
        </div>

        {/* ========================================
            KILL CHAIN SECTION
            ======================================== */}
        <div className="killchain-section">
          <div className="section-header">
            <h2>🎯 Individua la fase della Cyber Kill Chain</h2>
          </div>

          <div className="phases-container">
            {KILL_CHAIN_PHASES.map((phase, index) => {
              const maxPhases = DIFFICULTY_CONFIG[difficulty]?.phases || 7
              const isDisabled = index >= maxPhases || isLoading

              return (
                <div
                  key={phase.id}
                  className={`phase-card ${
                    selectedPhase === phase.id ? 'selected' : ''
                  } ${isDisabled ? 'disabled' : ''}`}
                  onClick={() => {
                    if (isDisabled) return
                    setSelectedPhase(phase.id)
                  }}
                  style={{
                    '--phase-color': phase.color
                  }}
                >
                  <div className="phase-number">{index + 1}</div>
                  <div className="phase-content">
                    <span className="phase-icon">{phase.icon}</span>
                    <h3>{phase.name}</h3>
                    <p>{phase.description}</p>
                  </div>
                </div>
              )
            })}
          </div>

          <button
            className="btn-submit"
            onClick={validatePhase}
            disabled={!selectedPhase || isLoading}
          >
            {isLoading ? 'Validazione...' : 'Procedi'}
          </button>
        </div>
      </div>
    </div>
  )
}