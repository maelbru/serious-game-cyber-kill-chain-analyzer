/*
 * CYBER KILL CHAIN ANALYZER - FRONTEND CORRETTO
 * Versione con bug fix e gestione errori robusta
 */

import { useState, useEffect, useCallback, useRef } from 'react'
import axios from 'axios'
import './App.css'

// ============================================================================
// CONFIGURAZIONE CON FALLBACK
// ============================================================================

const API_URL = 'http://localhost:5000/api'
const SESSION_ID = 'user_' + Math.random().toString(36).substr(2, 9)

// Timeout per le richieste API
const API_TIMEOUT = 5000

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

// Fallback logs per quando il backend non è disponibile
const FALLBACK_LOGS = [
  {
    id: 'fallback_recon',
    raw: 'Multiple DNS queries detected from external IP 185.234.218.12 for domain controllers and mail servers. Pattern suggests automated reconnaissance.',
    source: 'Network IDS',
    severity: 'Medium',
    timestamp: new Date().toISOString(),
    metadata: {
      source_ip: '185.234.218.12',
      queries: 47,
      targets: ['dc01.company.local', 'mail.company.local']
    }
  },
  {
    id: 'fallback_delivery',
    raw: 'Phishing campaign detected: 47 emails sent from "noreply@companysupport.tk" with malicious links to credential harvesting site.',
    source: 'Email Security',
    severity: 'High',
    timestamp: new Date().toISOString(),
    metadata: {
      sender: 'noreply@companysupport.tk',
      recipients: 47,
      malicious_url: 'company-login.tk'
    }
  }
]

const FALLBACK_MITIGATIONS = [
  {
    id: 'mit_1',
    name: 'Network Monitoring',
    description: 'Monitor network traffic for suspicious patterns',
    icon: '📡',
    effectiveness: 'High'
  },
  {
    id: 'mit_2',
    name: 'Email Filtering',
    description: 'Filter malicious emails and attachments',
    icon: '📧',
    effectiveness: 'Very High'
  },
  {
    id: 'mit_3',
    name: 'User Training',
    description: 'Train users to recognize security threats',
    icon: '🎓',
    effectiveness: 'Medium'
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
  const [gameState, setGameState] = useState('welcome')
  const [difficulty, setDifficulty] = useState('beginner')
  const [isBackendAvailable, setIsBackendAvailable] = useState(true)

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
  const [timeRemaining, setTimeRemaining] = useState(70)
  const [selectedPhase, setSelectedPhase] = useState(null)
  const [selectedMitigation, setSelectedMitigation] = useState(null)
  const [mitigationStrategies, setMitigationStrategies] = useState([])

  // Stati UI e feedback
  const [feedback, setFeedback] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [showTutorial, setShowTutorial] = useState(false)
  const [achievements, setAchievements] = useState([])
  const [error, setError] = useState(null)

  // Timer e refs
  const timerRef = useRef(null)
  const [isTimerActive, setIsTimerActive] = useState(false)
  const abortControllerRef = useRef(null)

  // ========================================
  // FUNZIONI HELPER CON VALIDAZIONE
  // ========================================

  const calculateDifficulty = useCallback(() => {
    try {
      const performanceScore = (score * 0.3) + (streak * 10) + (accuracy * 0.4)

      if (performanceScore < 50) return 'beginner'
      if (performanceScore < 150) return 'intermediate'
      return 'expert'
    } catch (error) {
      console.error('Error calculating difficulty:', error)
      return 'beginner'
    }
  }, [score, streak, accuracy])

  // Funzione per validare la risposta del server
  const validateApiResponse = (data, requiredFields = []) => {
    if (!data || typeof data !== 'object') return false

    return requiredFields.every(field => {
      const keys = field.split('.')
      let current = data
      for (const key of keys) {
        if (!current || !current.hasOwnProperty(key)) return false
        current = current[key]
      }
      return true
    })
  }

  // Funzione per gestire errori API
  const handleApiError = (error, fallbackAction = null) => {
    console.error('API Error:', error)

    if (error.code === 'ECONNREFUSED' || error.message?.includes('Network Error')) {
      setIsBackendAvailable(false)
      setError('Backend non disponibile. Usando modalità offline.')

      if (fallbackAction) {
        setTimeout(fallbackAction, 1000)
      }
    } else {
      setError(error.response?.data?.error || error.message || 'Errore sconosciuto')
    }
  }

  // ========================================
  // FUNZIONI API CON FALLBACK
  // ========================================

  const fetchNewLog = useCallback(async () => {
    setIsLoading(true)
    setSelectedPhase(null)
    setSelectedMitigation(null)
    setMitigationStrategies([])
    setError(null)

    const newDifficulty = calculateDifficulty()
    setDifficulty(newDifficulty)

    // Cancella richiesta precedente se in corso
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    abortControllerRef.current = new AbortController()

    try {
      const response = await axios.post(`${API_URL}/get-log`, {
        session_id: SESSION_ID,
        difficulty: newDifficulty,
        stats: { score, streak, accuracy }
      }, {
        timeout: API_TIMEOUT,
        signal: abortControllerRef.current.signal
      })

      if (validateApiResponse(response.data, ['log.id', 'log.raw', 'time_limit'])) {
        setCurrentLog(response.data.log)
        setTimeRemaining(response.data.time_limit || 70)
        setIsTimerActive(true)
        setGameState('playing')
        setIsBackendAvailable(true)
      } else {
        throw new Error('Invalid response format from server')
      }
    } catch (error) {
      if (error.name === 'AbortError') return // Richiesta cancellata

      handleApiError(error, () => {
        // Fallback con log locale
        const fallbackLog = FALLBACK_LOGS[Math.floor(Math.random() * FALLBACK_LOGS.length)]
        setCurrentLog({
          ...fallbackLog,
          timestamp: new Date().toISOString()
        })
        setTimeRemaining(70)
        setIsTimerActive(true)
        setGameState('playing')
      })
    } finally {
      setIsLoading(false)
    }
  }, [score, streak, accuracy, calculateDifficulty])

  const proceedFromTutorial = () => {
    setShowTutorial(false)
    setGameState('welcome')
  }

  // ========================================
  // VALIDAZIONE FASE CON FALLBACK
  // ========================================

  const validatePhase = useCallback(async () => {
    if (!selectedPhase) {
      setError('Nessuna fase selezionata')
      return
    }

    setIsTimerActive(false)
    setIsLoading(true)
    setError(null)

    try {
      if (isBackendAvailable) {
        const response = await axios.post(`${API_URL}/validate-phase`, {
          session_id: SESSION_ID,
          selected_phase: selectedPhase
        }, { timeout: API_TIMEOUT })

        if (validateApiResponse(response.data, ['is_correct'])) {
          if (response.data.is_correct) {
            // Fase corretta - mostra strategie di mitigazione
            setMitigationStrategies(response.data.mitigation_strategies || FALLBACK_MITIGATIONS)
            setFeedback({
              type: 'phase_correct',
              explanation: response.data.explanation,
              indicators: response.data.indicators
            })
            setGameState('mitigation')

            // Aggiorna statistiche parziali
            const phaseCount = phasesCompleted[selectedPhase] || 0
            setPhasesCompleted(prev => ({ ...prev, [selectedPhase]: phaseCount + 1 }))

          } else {
            // Fase errata
            handleIncorrectPhase(response.data)
          }
        } else {
          throw new Error('Invalid response format')
        }
      } else {
        // Modalità offline - simulazione semplice
        const isCorrect = Math.random() > 0.3 // 70% di successo in modalità offline

        if (isCorrect) {
          setMitigationStrategies(FALLBACK_MITIGATIONS)
          setFeedback({
            type: 'phase_correct',
            explanation: 'Risposta corretta! (Modalità offline)',
            indicators: ['Indicatore simulato']
          })
          setGameState('mitigation')
        } else {
          handleIncorrectPhase({
            correct_phase: 'reconnaissance',
            phase_info: KILL_CHAIN_PHASES[0],
            explanation: 'Risposta non corretta. (Modalità offline)',
            indicators: ['Prova a considerare gli indicatori di rete']
          })
        }
      }
    } catch (error) {
      handleApiError(error, () => {
        // Fallback per validazione fase
        setMitigationStrategies(FALLBACK_MITIGATIONS)
        setFeedback({
          type: 'phase_correct',
          explanation: 'Modalità offline attiva',
          indicators: ['Fallback mode']
        })
        setGameState('mitigation')
      })
    } finally {
      setIsLoading(false)
    }
  }, [selectedPhase, isBackendAvailable, phasesCompleted])

  // Funzione helper per gestire fase incorretta
  const handleIncorrectPhase = (responseData) => {
    setStreak(0)
    setTotalAttempts(prev => {
      const newTotal = prev + 1
      // Aggiorna accuracy in modo atomico
      setAccuracy(Math.round((correctAttempts / newTotal) * 100))
      return newTotal
    })

    setFeedback({
      type: 'phase_incorrect',
      correct_phase: responseData.correct_phase,
      phase_info: responseData.phase_info,
      explanation: responseData.explanation,
      indicators: responseData.indicators
    })
    setGameState('phase_feedback')
  }

  // ========================================
  // VALIDAZIONE MITIGAZIONE CON FALLBACK
  // ========================================

  const validateMitigation = useCallback(async () => {
    if (!selectedMitigation) {
      setError('Nessuna mitigazione selezionata')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      if (isBackendAvailable) {
        const response = await axios.post(`${API_URL}/validate-mitigation`, {
          session_id: SESSION_ID,
          selected_mitigation: selectedMitigation,
          time_remaining: timeRemaining,
          difficulty
        }, { timeout: API_TIMEOUT })

        if (validateApiResponse(response.data, ['is_correct', 'points'])) {
          handleMitigationResult(response.data)
        } else {
          throw new Error('Invalid response format')
        }
      } else {
        // Modalità offline - simulazione
        const isCorrect = Math.random() > 0.4 // 60% successo
        const points = isCorrect ? 25 + Math.floor(timeRemaining * 0.5) : 5

        handleMitigationResult({
          is_correct: isCorrect,
          points: points,
          selected_effectiveness: 'High',
          best_mitigation: FALLBACK_MITIGATIONS[0]
        })
      }
    } catch (error) {
      handleApiError(error, () => {
        // Fallback per mitigazione
        handleMitigationResult({
          is_correct: true,
          points: 15,
          selected_effectiveness: 'Medium',
          best_mitigation: FALLBACK_MITIGATIONS[0]
        })
      })
    } finally {
      setIsLoading(false)
    }
  }, [selectedMitigation, timeRemaining, difficulty, isBackendAvailable])

  // Funzione helper per gestire risultato mitigazione
  const handleMitigationResult = (result) => {
    const points = result.points || 0

    // Aggiorna statistiche in modo atomico
    setScore(prev => prev + points)

    setTotalAttempts(prev => {
      const newTotal = prev + 1
      const newCorrect = result.is_correct ? correctAttempts + 1 : correctAttempts

      if (result.is_correct) {
        setCorrectAttempts(newCorrect)
        setStreak(prev => prev + 1)
      } else {
        setStreak(0)
      }

      setAccuracy(Math.round((newCorrect / newTotal) * 100))
      return newTotal
    })

    // Check level up
    if (score + points >= level * 100) {
      setLevel(prev => prev + 1)
    }

    // Check achievements
    if (result.is_correct) {
      checkAchievements(streak + 1, score + points)
    }

    setFeedback({
      type: 'final',
      is_correct: result.is_correct,
      points: points,
      selected_effectiveness: result.selected_effectiveness,
      best_mitigation: result.best_mitigation
    })

    setGameState('final_feedback')
  }

  // ========================================
  // ACHIEVEMENTS SYSTEM
  // ========================================

  const checkAchievements = useCallback((currentStreak, currentScore) => {
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
      setAchievements(prev => [...prev, ...newAchievements])
      // TODO: Mostra notifica achievement
    }
  }, [achievements, phasesCompleted])

  // ========================================
  // TIMER EFFECT CON CLEANUP
  // ========================================

  useEffect(() => {
    let timeoutId = null

    if (isTimerActive && timeRemaining > 0 && gameState === 'playing') {
      timeoutId = setTimeout(() => {
        setTimeRemaining(prev => prev - 1)
      }, 1000)
    } else if (timeRemaining === 0 && isTimerActive && gameState === 'playing') {
      setIsTimerActive(false)

      // MODIFICA PRINCIPALE: Gestione specifica per timeout
      setFeedback({
        type: 'timeout',
        title: 'Tempo Scaduto!',
        message: 'Il tempo è scaduto prima che tu potessi selezionare una fase.',
        explanation: 'Ricorda di analizzare rapidamente il log e identificare gli indicatori chiave per la fase della Cyber Kill Chain.',
        showCorrectAnswer: false
      })
      setGameState('phase_feedback')

      // Aggiorna statistiche per timeout
      setStreak(0)
      setTotalAttempts(prev => {
        const newTotal = prev + 1
        setAccuracy(Math.round((correctAttempts / newTotal) * 100))
        return newTotal
      })
    }

    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId)
      }
    }
  }, [timeRemaining, isTimerActive, gameState, correctAttempts])

  // ========================================
  // CLEANUP EFFECT
  // ========================================

  useEffect(() => {
    return () => {
      // Cleanup al dismount del componente
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
      if (timerRef.current) {
        clearTimeout(timerRef.current)
      }
    }
  }, [])

  // ========================================
  // ERROR DISPLAY COMPONENT
  // ========================================

  const ErrorBanner = () => {
    if (!error) return null

    return (
      <div className="error-banner" onClick={() => setError(null)}>
        <span className="error-icon">⚠️</span>
        <span className="error-message">{error}</span>
        <span className="error-close">✕</span>
      </div>
    )
  }

  // ========================================
  // RENDERING UI
  // ========================================

  // SCHERMATA DI BENVENUTO
  if (gameState === 'welcome') {
    return (
      <div className="welcome-screen">
        <ErrorBanner />
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
            <button className="btn-secondary" onClick={() => setGameState('tutorial')}>
              📖 Tutorial
            </button>
          </div>
        </div>
      </div>
    )
  }

  // TUTORIAL SCREEN
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

  // Resto del rendering identico all'originale...
  // (FEEDBACK FASE INCORRETTA, SELEZIONE MITIGAZIONE, FEEDBACK FINALE, SCHERMATA PRINCIPALE)

  // FEEDBACK FASE INCORRETTA O TIMEOUT
  if (gameState === 'phase_feedback' && feedback) {
    return (
      <div className="modal-overlay">
        <ErrorBanner />
        <div className="feedback-modal">
          <div className={`feedback-icon ${feedback.type === 'timeout' ? 'warning' :
              feedback.type === 'phase_correct' ? 'success' : 'error'
            }`}>
            {feedback.type === 'timeout' ? '⏰' :
              feedback.type === 'phase_correct' ? '✓' : '✗'}
          </div>

          <h2 className="feedback-title">
            {feedback.type === 'timeout' ? 'Tempo Scaduto!' :
              feedback.type === 'phase_correct' ? 'Fase Corretta!' : 'Fase Non Corretta'}
          </h2>

          {/* Messaggio specifico per timeout */}
          {feedback.type === 'timeout' && (
            <div className="timeout-message">
              <p>{feedback.message}</p>
            </div>
          )}

          {/* Mostra risposta corretta solo se NON è timeout E c'è una risposta corretta */}
          {feedback.correct_phase && feedback.type !== 'timeout' && (
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
              <h4>📚 {feedback.type === 'timeout' ? 'Suggerimento:' : 'Spiegazione:'}</h4>
              <p>{feedback.explanation}</p>
            </div>
          )}

          {feedback.indicators && feedback.indicators.length > 0 && feedback.type !== 'timeout' && (
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
          {feedback.type === 'timeout' && (
            <div className="timeout-tips">
              <h4>💡 Consigli per il prossimo round:</h4>
              <ul>
                <li>Leggi rapidamente il log cercando parole chiave</li>
                <li>Identifica la fonte (Network, Email, Endpoint, etc.)</li>
                <li>Cerca indicatori di azione (scan, query, injection, etc.)</li>
                <li>Non overthinking - fidati del primo istinto</li>
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

  // SELEZIONE MITIGAZIONE
  if (gameState === 'mitigation') {
    return (
      <div className="game-container">
        <ErrorBanner />
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
        <ErrorBanner />
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

  // SCHERMATA DI GIOCO PRINCIPALE
  return (
    <div className="game-container">
      <ErrorBanner />

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

        {/* SEZIONE KILL CHAIN */}
        <div className="killchain-section">
          <div className="section-header">
            <h2>🎯 Identifica la Fase della Cyber Kill Chain</h2>
          </div>

          <div className="phases-container">
            {KILL_CHAIN_PHASES.map((phase, index) => {
              const isDisabled =
                (difficulty === 'beginner' && index > 2) ||
                (difficulty === 'intermediate' && index > 4) ||
                isLoading

              return (
                <div
                  key={phase.id}
                  className={`phase-card ${selectedPhase === phase.id ? 'selected' : ''} ${isDisabled ? 'disabled' : ''}`}
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
            {isLoading ? 'Validazione...' : 'Conferma Fase'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default App