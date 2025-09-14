/**
 * CYBER KILL CHAIN ANALYZER - CUSTOM HOOK PER LOGICA DI GIOCO
 * 
 * Questo è il cuore dell'applicazione: un custom hook React che incapsula
 * tutta la business logic del gioco, dalla gestione dello stato alle chiamate API.
 * 
 * Seguendo il pattern di separazione delle responsabilità, questo hook:
 * - Gestisce tutto lo stato del gioco 
 * - Si occupa delle comunicazioni con il backend
 * - Calcola punteggi e statistiche
 * - Gestisce timer e sessioni
 * - Fornisce funzioni per i componenti UI
 */

import { useState, useEffect, useCallback, useRef } from 'react'
import axios from 'axios'
import {
  API_URL,
  SESSION_ID,
  API_TIMEOUT,
  KILL_CHAIN_PHASES,
  FALLBACK_LOGS,
  FALLBACK_MITIGATIONS,
  ACHIEVEMENT_CONFIG,
  DIFFICULTY_CONFIG,
  GAME_STATES,
  FEEDBACK_TYPES
} from '../utils/constants.js'

export function useGameLogic() {
  // ========================================
  // STATO DEL GIOCO - GESTIONE CENTRALIZZATA
  // Tutti gli stati dell'applicazione sono centralizzati qui per facilità di gestione
  // ========================================

  // --- STATI GENERALI DEL GIOCO ---
  const [gameState, setGameState] = useState(GAME_STATES.WELCOME)  // Schermata corrente
  const [difficulty, setDifficulty] = useState('beginner')         // Livello di difficoltà
  const [isBackendAvailable, setIsBackendAvailable] = useState(true) // Se il server risponde

  // --- STATISTICHE E PROGRESSI DEL GIOCATORE ---
  const [score, setScore] = useState(0)                    // Punteggio totale accumulato
  const [streak, setStreak] = useState(0)                  // Serie di risposte corrette consecutive
  const [level, setLevel] = useState(1)                    // Livello del giocatore (basato su score)
  const [accuracy, setAccuracy] = useState(100)            // Percentuale di accuratezza
  const [totalAttempts, setTotalAttempts] = useState(0)    // Numero totale di tentativi
  const [correctAttempts, setCorrectAttempts] = useState(0) // Numero di risposte corrette
  const [phasesCompleted, setPhasesCompleted] = useState({}) // Conteggio per fase per achievements

  // --- STATO DEL ROUND CORRENTE ---
  const [currentLog, setCurrentLog] = useState(null)                    // Log da analizzare
  const [timeRemaining, setTimeRemaining] = useState(60)                // Secondi rimasti
  const [selectedPhase, setSelectedPhase] = useState(null)              // Fase scelta dall'utente
  const [selectedMitigation, setSelectedMitigation] = useState(null)    // Mitigazione scelta
  const [mitigationStrategies, setMitigationStrategies] = useState([]) // Opzioni di mitigazione disponibili

  // --- STATI DELL'INTERFACCIA E FEEDBACK ---
  const [feedback, setFeedback] = useState(null)          // Dati del feedback da mostrare
  const [isLoading, setIsLoading] = useState(false)       // Se è in corso un caricamento
  const [achievements, setAchievements] = useState([])     // Lista degli achievements sbloccati
  const [error, setError] = useState(null)                // Messaggi di errore da mostrare

  // --- CONTROLLO TIMER E RICHIESTE ---
  const [isTimerActive, setIsTimerActive] = useState(false) // Se il timer è attivo
  const abortControllerRef = useRef(null)                  // Per cancellare richieste HTTP

  // ========================================
  // FUNZIONI DI SUPPORTO E CALCOLI
  // ========================================

  /**
   * Calcola dinamicamente la difficoltà basata sulle performance del giocatore
   */
  const calculateDifficulty = useCallback(() => {
    try {
      // Formula che combina score, streak e accuracy per determinare il livello
      const performanceScore = (score * 0.3) + (streak * 10) + (accuracy * 0.4)
      if (performanceScore < 50) return 'beginner'
      if (performanceScore < 150) return 'intermediate'
      return 'expert'
    } catch (error) {
      console.error('Error calculating difficulty:', error)
      return 'beginner' // Fallback sicuro
    }
  }, [score, streak, accuracy])

  /**
   * Verifica che la risposta dal server contenga i campi richiesti
   */
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

  /**
   * Gestisce gli errori delle chiamate API con messaggi user-friendly
   */
  const handleApiError = (error, fallbackAction = null) => {
    console.error('API Error:', error)

    // Gestione specifica per diversi tipi di errore
    if (error.response?.status === 429) {
      // Rate limiting
      setError('⏰ Troppi tentativi! Riprova tra qualche minuto.')
      setIsBackendAvailable(false)
    } else if (error.response?.status === 400) {
      // Errore di validazione
      const errorMsg = error.response.data?.error || 'Dati non validi forniti'
      setError(`❌ ${errorMsg}`)
    } else if (error.code === 'ECONNREFUSED' || error.message?.includes('Network Error')) {
      // Backend non raggiungibile - attiva modalità offline
      setIsBackendAvailable(false)
      setError('📡 Backend non disponibile. Usando modalità offline.')
      if (fallbackAction) {
        setTimeout(fallbackAction, 1000) // Esegui fallback dopo 1 secondo
      }
    } else {
      // Altri errori generici
      setError(`⚠️ ${error.response?.data?.error || error.message || 'Errore sconosciuto'}`)
    }
  }

  // ========================================
  // FUNZIONI PER CHIAMATE API
  // ========================================

  /**
   * Ottiene un nuovo log di sicurezza dal backend per iniziare un nuovo round
   */
  const fetchNewLog = useCallback(async () => {
    // Prepara l'UI per il caricamento
    setIsLoading(true)
    setSelectedPhase(null)
    setSelectedMitigation(null)
    setMitigationStrategies([])
    setError(null)

    // Calcola difficoltà dinamica
    const newDifficulty = calculateDifficulty()
    setDifficulty(newDifficulty)

    // Cancella eventuali richieste precedenti ancora in corso
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    abortControllerRef.current = new AbortController()

    try {
      // Chiamata al backend per ottenere un nuovo log
      const response = await axios.post(`${API_URL}/get-log`, {
        session_id: SESSION_ID,
        difficulty: newDifficulty,
        stats: { score, streak, accuracy }  // Invia stats per difficoltà dinamica
      }, {
        timeout: API_TIMEOUT,
        signal: abortControllerRef.current.signal // Per cancellazione richiesta
      })

      // Verifica che la risposta sia valida
      if (validateApiResponse(response.data, ['log.id', 'log.raw', 'time_limit'])) {
        // Successo - configura il nuovo round
        setCurrentLog(response.data.log)
        setTimeRemaining(response.data.time_limit || 60)
        setIsTimerActive(true)  // Avvia il timer
        setGameState(GAME_STATES.PLAYING)
        setIsBackendAvailable(true)
      } else {
        throw new Error('Invalid response format from server')
      }
    } catch (error) {
      // Non gestire errori se la richiesta è stata cancellata
      if (error.name === 'AbortError') return

      // Gestisci l'errore e attiva modalità offline se necessario
      handleApiError(error, () => {
        // Fallback: usa un log di esempio
        const fallbackLog = FALLBACK_LOGS[Math.floor(Math.random() * FALLBACK_LOGS.length)]
        setCurrentLog({
          ...fallbackLog,
          timestamp: new Date().toISOString()
        })
        setTimeRemaining(DIFFICULTY_CONFIG[newDifficulty]?.timeLimit || 60)
        setIsTimerActive(true)
        setGameState(GAME_STATES.PLAYING)
      })
    } finally {
      setIsLoading(false)
    }
  }, [score, streak, accuracy, calculateDifficulty])

  /**
   * Valida la fase della Kill Chain selezionata dall'utente
   */
  const validatePhase = useCallback(async () => {
    if (!selectedPhase) {
      setError('Nessuna fase selezionata')
      return
    }

    // Ferma il timer e prepara per la validazione
    setIsTimerActive(false)
    setIsLoading(true)
    setError(null)

    try {
      if (isBackendAvailable) {
        // Chiamata al backend per la validazione
        const response = await axios.post(`${API_URL}/validate-phase`, {
          session_id: SESSION_ID,
          selected_phase: selectedPhase
        }, { timeout: API_TIMEOUT })

        if (validateApiResponse(response.data, ['is_correct'])) {
          if (response.data.is_correct) {
            // RISPOSTA CORRETTA - Procedi alla selezione mitigazione
            setMitigationStrategies(response.data.mitigation_strategies || FALLBACK_MITIGATIONS)
            setFeedback({
              type: FEEDBACK_TYPES.PHASE_CORRECT,
              explanation: response.data.explanation,
              indicators: response.data.indicators
            })
            setGameState(GAME_STATES.MITIGATION)

            // Aggiorna conteggio fasi per achievements
            const phaseCount = phasesCompleted[selectedPhase] || 0
            setPhasesCompleted(prev => ({ ...prev, [selectedPhase]: phaseCount + 1 }))
          } else {
            // RISPOSTA SBAGLIATA - Mostra feedback educativo
            handleIncorrectPhase(response.data)
          }
        } else {
          throw new Error('Invalid response format')
        }
      } else {
        // MODALITÀ OFFLINE - Simula la validazione
        const isCorrect = Math.random() > 0.3 // 70% di probabilità di successo

        if (isCorrect) {
          setMitigationStrategies(FALLBACK_MITIGATIONS)
          setFeedback({
            type: FEEDBACK_TYPES.PHASE_CORRECT,
            explanation: 'Risposta corretta! (Modalità offline)',
            indicators: ['Indicatore simulato']
          })
          setGameState(GAME_STATES.MITIGATION)
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
      // Errore nella validazione - usa fallback
      handleApiError(error, () => {
        setMitigationStrategies(FALLBACK_MITIGATIONS)
        setFeedback({
          type: FEEDBACK_TYPES.PHASE_CORRECT,
          explanation: 'Modalità offline attiva',
          indicators: ['Fallback mode']
        })
        setGameState(GAME_STATES.MITIGATION)
      })
    } finally {
      setIsLoading(false)
    }
  }, [selectedPhase, isBackendAvailable, phasesCompleted])

  /**
   * Valida la strategia di mitigazione selezionata e calcola il punteggio
   */
  const validateMitigation = useCallback(async () => {
    if (!selectedMitigation) {
      setError('Nessuna mitigazione selezionata')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      if (isBackendAvailable) {
        // Chiamata al backend per validare mitigazione
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
        // MODALITÀ OFFLINE - Simula il risultato
        const isCorrect = Math.random() > 0.4 // 60% probabilità successo
        const points = isCorrect ? 25 + Math.floor(timeRemaining * 0.5) : 5

        handleMitigationResult({
          is_correct: isCorrect,
          points: points,
          selected_effectiveness: 'High',
          best_mitigation: FALLBACK_MITIGATIONS[0]
        })
      }
    } catch (error) {
      // Errore - usa risultato di fallback
      handleApiError(error, () => {
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

  // ========================================
  // FUNZIONI DI SUPPORTO PER LA VALIDAZIONE
  // ========================================

  /**
   * Gestisce il caso di fase identificata incorrettamente
   */
  const handleIncorrectPhase = (responseData) => {
    // Reset streak e aggiorna statistiche
    setStreak(0)
    setTotalAttempts(prev => {
      const newTotal = prev + 1
      setAccuracy(Math.round((correctAttempts / newTotal) * 100))
      return newTotal
    })

    // Imposta feedback educativo
    setFeedback({
      type: FEEDBACK_TYPES.PHASE_INCORRECT,
      correct_phase: responseData.correct_phase,
      phase_info: responseData.phase_info,
      explanation: responseData.explanation,
      indicators: responseData.indicators
    })
    setGameState(GAME_STATES.PHASE_FEEDBACK)
  }

  /**
   * Gestisce il risultato della validazione della mitigazione
   */
  const handleMitigationResult = (result) => {
    const points = result.points || 0

    // Aggiorna punteggio
    setScore(prev => prev + points)
    
    // Aggiorna statistiche e streak
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

    // Level up se ha abbastanza punti
    if (score + points >= level * 100) {
      setLevel(prev => prev + 1)
    }

    // Controlla achievements se ha risposto correttamente
    if (result.is_correct) {
      checkAchievements(streak + 1, score + points)
    }

    // Imposta feedback finale
    setFeedback({
      type: FEEDBACK_TYPES.FINAL,
      is_correct: result.is_correct,
      points: points,
      selected_effectiveness: result.selected_effectiveness,
      best_mitigation: result.best_mitigation
    })

    setGameState(GAME_STATES.FINAL_FEEDBACK)
  }

  // ========================================
  // SISTEMA ACHIEVEMENTS
  // ========================================

  /**
   * Controlla se il giocatore ha sbloccato nuovi achievements
   */
  const checkAchievements = useCallback((currentStreak, currentScore) => {
    const newAchievements = []

    // Achievement basati su streak
    if (currentStreak === 5 && !achievements.includes('streak_5')) {
      newAchievements.push('streak_5')
    }
    if (currentStreak === 10 && !achievements.includes('streak_10')) {
      newAchievements.push('streak_10')
    }
    
    // Achievement basati su punteggio
    if (currentScore >= 500 && !achievements.includes('score_500')) {
      newAchievements.push('score_500')
    }
    if (currentScore >= 1000 && !achievements.includes('score_1000')) {
      newAchievements.push('score_1000')
    }

    // Achievement per maestria delle fasi
    const masteredPhases = Object.values(phasesCompleted).filter(count => count >= 3).length
    if (masteredPhases >= 4 && !achievements.includes('phase_master')) {
      newAchievements.push('phase_master')
    }

    // Aggiungi nuovi achievements alla lista
    if (newAchievements.length > 0) {
      setAchievements(prev => [...prev, ...newAchievements])
    }
  }, [achievements, phasesCompleted])

  // ========================================
  // GESTIONE TIMER CON useEffect
  // ========================================

  useEffect(() => {
    let timeoutId = null

    // Timer attivo e tempo rimanente - decrementa ogni secondo
    if (isTimerActive && timeRemaining > 0 && gameState === GAME_STATES.PLAYING) {
      timeoutId = setTimeout(() => {
        setTimeRemaining(prev => prev - 1)
      }, 1000)
    } 
    // Tempo scaduto - gestisci timeout
    else if (timeRemaining === 0 && isTimerActive && gameState === GAME_STATES.PLAYING) {
      setIsTimerActive(false)

      // Imposta feedback di timeout
      setFeedback({
        type: FEEDBACK_TYPES.TIMEOUT,
        title: 'Tempo Scaduto!',
        message: 'Il tempo è scaduto prima che tu potessi selezionare una fase.',
        explanation: 'Ricorda di analizzare rapidamente il log e identificare gli indicatori chiave per la fase della Cyber Kill Chain.',
        showCorrectAnswer: false
      })
      setGameState(GAME_STATES.PHASE_FEEDBACK)

      // Reset streak e aggiorna statistiche per timeout
      setStreak(0)
      setTotalAttempts(prev => {
        const newTotal = prev + 1
        setAccuracy(Math.round((correctAttempts / newTotal) * 100))
        return newTotal
      })
    }

    // Cleanup del timeout
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId)
      }
    }
  }, [timeRemaining, isTimerActive, gameState, correctAttempts])

  // ========================================
  // CLEANUP GENERALE
  // ========================================

  useEffect(() => {
    // Cleanup quando il componente viene smontato
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  // ========================================
  // API PUBBLICA DEL HOOK
  // Restituisce tutti gli stati e funzioni necessarie ai componenti
  // ========================================

  return {
    // Stati del gioco
    gameState,
    setGameState,
    difficulty,
    isBackendAvailable,

    // Statistiche del giocatore
    score,
    streak, 
    level,
    accuracy,
    totalAttempts,
    correctAttempts,
    achievements,

    // Dati del round corrente
    currentLog,
    timeRemaining,
    selectedPhase,
    setSelectedPhase,
    selectedMitigation,
    setSelectedMitigation,
    mitigationStrategies,

    // Stati dell'interfaccia
    feedback,
    isLoading,
    error,
    setError,
    isTimerActive,

    // Funzioni di azione
    fetchNewLog,
    validatePhase,
    validateMitigation,

    // Dati di supporto
    phasesCompleted
  }
}