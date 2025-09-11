/*
 * CYBER KILL CHAIN ANALYZER - FRONTEND
 * Serious game per l'apprendimento delle fasi della Cyber Kill Chain
 * e delle strategie di mitigazione appropriate
 */

import { useState, useEffect, useCallback, useRef } from 'react'
import axios from 'axios'
import './App.css'

// ============================================================================
// CONFIGURAZIONE
// ============================================================================

const API_URL = 'http://localhost:5000/api'
const SESSION_ID = 'user_' + Math.random().toString(36).substr(2, 9)

// ============================================================================
// DATI DELLE FASI CYBER KILL CHAIN
// ============================================================================

const KILL_CHAIN_PHASES = [
  {
    id: 'reconnaissance',
    name: 'Reconnaissance',
    icon: '🔍',
    description: 'Raccolta informazioni sul target',
    color: '#3b82f6'
  },
  {
    id: 'weaponization',
    name: 'Weaponization',
    icon: '🔨',
    description: 'Creazione del payload malevolo',
    color: '#8b5cf6'
  },
  {
    id: 'delivery',
    name: 'Delivery',
    icon: '📧',
    description: 'Consegna del malware al target',
    color: '#ec4899'
  },
  {
    id: 'exploitation',
    name: 'Exploitation',
    icon: '💥',
    description: 'Sfruttamento delle vulnerabilità',
    color: '#f59e0b'
  },
  {
    id: 'installation',
    name: 'Installation',
    icon: '⚙️',
    description: 'Installazione del malware',
    color: '#10b981'
  },
  {
    id: 'command_control',
    name: 'Command & Control',
    icon: '📡',
    description: 'Controllo remoto del sistema',
    color: '#06b6d4'
  },
  {
    id: 'actions_objectives',
    name: 'Actions on Objectives',
    icon: '🎯',
    description: 'Raggiungimento degli obiettivi',
    color: '#ef4444'
  }
]

// ============================================================================
// COMPONENTE PRINCIPALE
// ============================================================================

function App() {
  // ========================================
  // STATE MANAGEMENT
  // ========================================

  // Stati generali del gioco
  const [gameState, setGameState] = useState('welcome') // welcome, playing, phase_feedback, mitigation, final_feedback
  const [difficulty, setDifficulty] = useState('beginner')

  // Statistiche giocatore
  const [score, setScore] = useState(0)
  const [streak, setStreak] = useState(0)
  const [level, setLevel] = useState(1)
  const [accuracy, setAccuracy] = useState(100)
  const [totalAttempts, setTotalAttempts] = useState(0)
  const [correctAttempts, setCorrectAttempts] = useState(0)
  const [phasesCompleted, setPhasesCompleted] = useState({})

  // Stati del round corrente
  const [currentLog, setCurrentLog] = useState(null)
  const [timeRemaining, setTimeRemaining] = useState(90)
  const [selectedPhase, setSelectedPhase] = useState(null)
  const [selectedMitigation, setSelectedMitigation] = useState(null)
  const [mitigationStrategies, setMitigationStrategies] = useState([])

  // Stati UI e feedback
  const [feedback, setFeedback] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showTutorial, setShowTutorial] = useState(false)
  const [achievements, setAchievements] = useState([])

  // Timer
  const timerRef = useRef(null)
  const [isTimerActive, setIsTimerActive] = useState(false)

  // ========================================
  // FUNZIONI HELPER
  // ========================================

  const calculateDifficulty = useCallback(() => {
    const performanceScore = (score * 0.3) + (streak * 10) + (accuracy * 0.4)

    if (performanceScore < 50) return 'beginner'
    if (performanceScore < 150) return 'intermediate'
    return 'expert'
  }, [score, streak, accuracy])

  // ========================================
  // FETCH NUOVO LOG
  // ========================================

  const fetchNewLog = useCallback(async () => {
    setIsLoading(true)
    setSelectedPhase(null)
    setSelectedMitigation(null)
    setMitigationStrategies([])

    const newDifficulty = calculateDifficulty()
    setDifficulty(newDifficulty)

    try {
      const response = await axios.post(`${API_URL}/get-log`, {
        session_id: SESSION_ID,
        difficulty: newDifficulty,
        stats: { score, streak, accuracy }
      })

      if (response.data && response.data.log) {
        setCurrentLog(response.data.log)
        setTimeRemaining(response.data.time_limit || 90)
        setIsTimerActive(true)
        setGameState('playing')
      }
    } catch (error) {
      console.error('Error fetching log:', error)
      // Fallback per test
      setCurrentLog({
        id: 'test_1',
        raw: 'Test log: Multiple DNS queries detected from external IP for domain controllers and mail servers.',
        source: 'Test System',
        severity: 'Medium',
        timestamp: new Date().toISOString()
      })
      setTimeRemaining(90)
      setIsTimerActive(true)
      setGameState('playing')
    } finally {
      setIsLoading(false)
    }
  }, [score, streak, accuracy, calculateDifficulty])

  const proceedFromTutorial = () => {
    setShowTutorial(false)
    setGameState('welcome')
  }

  // ========================================
  // VALIDAZIONE FASE
  // ========================================

  const validatePhase = async () => {
    if (!selectedPhase) return

    setIsTimerActive(false)
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_URL}/validate-phase`, {
        session_id: SESSION_ID,
        selected_phase: selectedPhase
      })

      if (response.data.is_correct) {
        // Fase corretta - mostra strategie di mitigazione
        setMitigationStrategies(response.data.mitigation_strategies || [])
        setFeedback({
          type: 'phase_correct',
          explanation: response.data.explanation,
          indicators: response.data.indicators
        })
        setGameState('mitigation')

        // Aggiorna statistiche parziali
        const phaseCount = phasesCompleted[selectedPhase] || 0
        setPhasesCompleted({ ...phasesCompleted, [selectedPhase]: phaseCount + 1 })

      } else {
        // Fase errata
        setStreak(0)
        setTotalAttempts(prev => prev + 1)

        setFeedback({
          type: 'phase_incorrect',
          correct_phase: response.data.correct_phase,
          phase_info: response.data.phase_info,
          explanation: response.data.explanation,
          indicators: response.data.indicators
        })
        setGameState('phase_feedback')
      }
    } catch (error) {
      console.error('Error validating phase:', error)
      setFeedback({
        type: 'error',
        message: 'Errore nella validazione. Riprova.'
      })
      setGameState('phase_feedback')
    } finally {
      setIsLoading(false)
    }
  }

  // ========================================
  // VALIDAZIONE MITIGAZIONE
  // ========================================

  const validateMitigation = async () => {
    if (!selectedMitigation) return

    setIsLoading(true)

    try {
      const response = await axios.post(`${API_URL}/validate-mitigation`, {
        session_id: SESSION_ID,
        selected_mitigation: selectedMitigation,
        time_remaining: timeRemaining,
        difficulty
      })

      // Aggiorna statistiche complete
      const points = response.data.points || 0
      setScore(prev => prev + points)
      setTotalAttempts(prev => prev + 1)

      if (response.data.is_correct) {
        setStreak(prev => prev + 1)
        setCorrectAttempts(prev => prev + 1)

        // Check achievements
        checkAchievements(streak + 1, score + points)
      } else {
        setStreak(0)
      }

      // Ricalcola accuracy
      const newAccuracy = Math.round(((correctAttempts + (response.data.is_correct ? 1 : 0)) / (totalAttempts + 1)) * 100)
      setAccuracy(newAccuracy)

      // Check level up
      if (score + points >= level * 100) {
        setLevel(prev => prev + 1)
      }

      setFeedback({
        type: 'final',
        is_correct: response.data.is_correct,
        points: points,
        selected_effectiveness: response.data.selected_effectiveness,
        best_mitigation: response.data.best_mitigation
      })

      setGameState('final_feedback')

    } catch (error) {
      console.error('Error validating mitigation:', error)
      setFeedback({
        type: 'error',
        message: 'Errore nella validazione della mitigazione.'
      })
      setGameState('final_feedback')
    } finally {
      setIsLoading(false)
    }
  }

  // ========================================
  // ACHIEVEMENTS SYSTEM
  // ========================================

  const checkAchievements = (currentStreak, currentScore) => {
    const newAchievements = []

    // Streak achievements
    if (currentStreak === 5 && !achievements.includes('streak_5')) {
      newAchievements.push('streak_5')
    }
    if (currentStreak === 10 && !achievements.includes('streak_10')) {
      newAchievements.push('streak_10')
    }

    // Score achievements
    if (currentScore >= 500 && !achievements.includes('score_500')) {
      newAchievements.push('score_500')
    }
    if (currentScore >= 1000 && !achievements.includes('score_1000')) {
      newAchievements.push('score_1000')
    }

    // Phase mastery
    const masteredPhases = Object.values(phasesCompleted).filter(count => count >= 3).length
    if (masteredPhases >= 4 && !achievements.includes('phase_master')) {
      newAchievements.push('phase_master')
    }

    if (newAchievements.length > 0) {
      setAchievements([...achievements, ...newAchievements])
      // Mostra notifica achievement (TODO)
    }
  }

  // ========================================
  // TIMER EFFECT
  // ========================================

  useEffect(() => {
    if (isTimerActive && timeRemaining > 0) {
      timerRef.current = setTimeout(() => {
        setTimeRemaining(prev => prev - 1)
      }, 1000)
    } else if (timeRemaining === 0 && isTimerActive) {
      setIsTimerActive(false)
      if (gameState === 'playing') {
        validatePhase()
      }
    }

    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current)
        timerRef.current = null
      }
    }
  }, [timeRemaining, isTimerActive, gameState])

  // ========================================
  // RENDERING UI
  // ========================================

  // SCHERMATA DI BENVENUTO
  if (gameState === 'welcome') {
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
            <button className="btn-primary" onClick={fetchNewLog}>
              🎮 Inizia a Giocare
            </button>
            <button className="btn-secondary" onClick={() => setGameState('tutorial')}>
              📖 Tutorial
            </button>
          </div>
        </div>
      </div>
    )
  }

  // TUTORIAL SCREEN (ora parte del flusso principale)
  if (gameState === 'tutorial') {
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

          <div className="kill-chain-explanation">
            <h2>Le 7 Fasi della Cyber Kill Chain:</h2>
            <div className="phases-grid">
              {KILL_CHAIN_PHASES.map((phase, index) => (
                <div key={phase.id} className="phase-explanation">
                  <div className="phase-header">
                    <span className="phase-num">{index + 1}</span>
                    <span className="phase-emoji">{phase.icon}</span>
                    <span className="phase-title">{phase.name}</span>
                  </div>
                  <p className="phase-desc">{phase.description}</p>
                </div>
              ))}
            </div>
          </div>

          <button className="btn-start-game" onClick={proceedFromTutorial}>
            Capito! Iniziamo 🚀
          </button>
        </div>
      </div>
    )
  }

  // FEEDBACK FASE INCORRETTA
  if (gameState === 'phase_feedback' && feedback) {
    return (
      <div className="modal-overlay">
        <div className="feedback-modal">
          <div className={`feedback-icon ${feedback.type === 'phase_correct' ? 'success' : 'error'}`}>
            {feedback.type === 'phase_correct' ? '✓' : '✗'}
          </div>

          <h2 className="feedback-title">
            {feedback.type === 'phase_correct' ? 'Fase Corretta!' : 'Fase Non Corretta'}
          </h2>

          {feedback.correct_phase && (
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
              <h4>📚 Spiegazione:</h4>
              <p>{feedback.explanation}</p>
            </div>
          )}

          {feedback.indicators && feedback.indicators.length > 0 && (
            <div className="indicators-box">
              <h4>🔍 Indicatori Chiave:</h4>
              <ul>
                {feedback.indicators.map((indicator, idx) => (
                  <li key={idx}>{indicator}</li>
                ))}
              </ul>
            </div>
          )}

          <button className="btn-primary" onClick={fetchNewLog}>
            Prossimo Log →
          </button>
        </div>
      </div>
    )
  }

  // SELEZIONE MITIGAZIONE
  if (gameState === 'mitigation') {
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

  // FEEDBACK FINALE
  if (gameState === 'final_feedback' && feedback) {
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
              <p>La tua scelta aveva efficacia: <strong>{feedback.selected_effectiveness}</strong></p>
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
            <h4>Progressi:</h4>
            <div className="progress-stats">
              <div className="progress-item">
                <span>Score Totale:</span>
                <span>{score}</span>
              </div>
              <div className="progress-item">
                <span>Accuracy:</span>
                <span>{accuracy}%</span>
              </div>
              <div className="progress-item">
                <span>Livello:</span>
                <span>{level}</span>
              </div>
            </div>
          </div>

          <button className="btn-primary" onClick={fetchNewLog}>
            Continua →
          </button>
        </div>
      </div>
    )
  }

  // SCHERMATA DI GIOCO PRINCIPALE
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
        </div>
      </header>

      <div className="game-content">
        {/* SEZIONE LOG */}
        <div className="log-section">
          <div className="section-header">
            <h2>📋 Security Log Analysis</h2>
            <div className={`timer ${timeRemaining <= 15 ? 'critical' : timeRemaining <= 30 ? 'warning' : ''}`}>
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

              {currentLog.metadata && (
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
        </div>

        {/* SEZIONE KILL CHAIN */}
        <div className="killchain-section">
          <div className="section-header">
            <h2>🎯 Identifica la Fase della Cyber Kill Chain</h2>
          </div>

          <div className="phases-container">
            {KILL_CHAIN_PHASES.map((phase, index) => (
              <div
                key={phase.id}
                className={`phase-card ${selectedPhase === phase.id ? 'selected' : ''} ${difficulty === 'beginner' && index > 2 ? 'disabled' : ''
                  } ${difficulty === 'intermediate' && index > 4 ? 'disabled' : ''}`}
                onClick={() => {
                  if (difficulty === 'beginner' && index > 2) return
                  if (difficulty === 'intermediate' && index > 4) return
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
            ))}
          </div>

          <button
            className="btn-submit"
            onClick={validatePhase}
            disabled={!selectedPhase || isLoading}
          >
            {isLoading ? 'Validazione...' : 'Conferma Fase'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default App