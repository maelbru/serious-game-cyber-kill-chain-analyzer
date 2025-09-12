/**
 * CYBER KILL CHAIN ANALYZER - GAME LOGIC HOOK
 * Custom hook che gestisce tutta la business logic del gioco
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
  // STATE MANAGEMENT
  // ========================================

  // Stati generali del gioco
  const [gameState, setGameState] = useState(GAME_STATES.WELCOME)
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
  const [timeRemaining, setTimeRemaining] = useState(60)
  const [selectedPhase, setSelectedPhase] = useState(null)
  const [selectedMitigation, setSelectedMitigation] = useState(null)
  const [mitigationStrategies, setMitigationStrategies] = useState([])

  // Stati UI e feedback
  const [feedback, setFeedback] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [achievements, setAchievements] = useState([])
  const [error, setError] = useState(null)

  // Timer e refs
  const [isTimerActive, setIsTimerActive] = useState(false)
  const abortControllerRef = useRef(null)

  // ========================================
  // HELPER FUNCTIONS
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
  // API FUNCTIONS
  // ========================================

  const fetchNewLog = useCallback(async () => {
    setIsLoading(true)
    setSelectedPhase(null)
    setSelectedMitigation(null)
    setMitigationStrategies([])
    setError(null)

    const newDifficulty = calculateDifficulty()
    setDifficulty(newDifficulty)

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
        setTimeRemaining(response.data.time_limit || 60)
        setIsTimerActive(true)
        setGameState(GAME_STATES.PLAYING)
        setIsBackendAvailable(true)
      } else {
        throw new Error('Invalid response format from server')
      }
    } catch (error) {
      if (error.name === 'AbortError') return

      handleApiError(error, () => {
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
            setMitigationStrategies(response.data.mitigation_strategies || FALLBACK_MITIGATIONS)
            setFeedback({
              type: FEEDBACK_TYPES.PHASE_CORRECT,
              explanation: response.data.explanation,
              indicators: response.data.indicators
            })
            setGameState(GAME_STATES.MITIGATION)

            const phaseCount = phasesCompleted[selectedPhase] || 0
            setPhasesCompleted(prev => ({ ...prev, [selectedPhase]: phaseCount + 1 }))
          } else {
            handleIncorrectPhase(response.data)
          }
        } else {
          throw new Error('Invalid response format')
        }
      } else {
        // Modalità offline
        const isCorrect = Math.random() > 0.3

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
        const isCorrect = Math.random() > 0.4
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
  // HELPER FUNCTIONS FOR VALIDATION
  // ========================================

  const handleIncorrectPhase = (responseData) => {
    setStreak(0)
    setTotalAttempts(prev => {
      const newTotal = prev + 1
      setAccuracy(Math.round((correctAttempts / newTotal) * 100))
      return newTotal
    })

    setFeedback({
      type: FEEDBACK_TYPES.PHASE_INCORRECT,
      correct_phase: responseData.correct_phase,
      phase_info: responseData.phase_info,
      explanation: responseData.explanation,
      indicators: responseData.indicators
    })
    setGameState(GAME_STATES.PHASE_FEEDBACK)
  }

  const handleMitigationResult = (result) => {
    const points = result.points || 0

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

    if (score + points >= level * 100) {
      setLevel(prev => prev + 1)
    }

    if (result.is_correct) {
      checkAchievements(streak + 1, score + points)
    }

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
  // ACHIEVEMENTS SYSTEM
  // ========================================

  const checkAchievements = useCallback((currentStreak, currentScore) => {
    const newAchievements = []

    if (currentStreak === 5 && !achievements.includes('streak_5')) {
      newAchievements.push('streak_5')
    }
    if (currentStreak === 10 && !achievements.includes('streak_10')) {
      newAchievements.push('streak_10')
    }
    if (currentScore >= 500 && !achievements.includes('score_500')) {
      newAchievements.push('score_500')
    }
    if (currentScore >= 1000 && !achievements.includes('score_1000')) {
      newAchievements.push('score_1000')
    }

    const masteredPhases = Object.values(phasesCompleted).filter(count => count >= 3).length
    if (masteredPhases >= 4 && !achievements.includes('phase_master')) {
      newAchievements.push('phase_master')
    }

    if (newAchievements.length > 0) {
      setAchievements(prev => [...prev, ...newAchievements])
    }
  }, [achievements, phasesCompleted])

  // ========================================
  // TIMER EFFECT
  // ========================================

  useEffect(() => {
    let timeoutId = null

    if (isTimerActive && timeRemaining > 0 && gameState === GAME_STATES.PLAYING) {
      timeoutId = setTimeout(() => {
        setTimeRemaining(prev => prev - 1)
      }, 1000)
    } else if (timeRemaining === 0 && isTimerActive && gameState === GAME_STATES.PLAYING) {
      setIsTimerActive(false)

      setFeedback({
        type: FEEDBACK_TYPES.TIMEOUT,
        title: 'Tempo Scaduto!',
        message: 'Il tempo è scaduto prima che tu potessi selezionare una fase.',
        explanation: 'Ricorda di analizzare rapidamente il log e identificare gli indicatori chiave per la fase della Cyber Kill Chain.',
        showCorrectAnswer: false
      })
      setGameState(GAME_STATES.PHASE_FEEDBACK)

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
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  // ========================================
  // PUBLIC API
  // ========================================

  return {
    // Game State
    gameState,
    setGameState,
    difficulty,
    isBackendAvailable,
    
    // Player Stats
    score,
    streak,
    level,
    accuracy,
    totalAttempts,
    correctAttempts,
    achievements,
    
    // Current Round
    currentLog,
    timeRemaining,
    selectedPhase,
    setSelectedPhase,
    selectedMitigation,
    setSelectedMitigation,
    mitigationStrategies,
    
    // UI State
    feedback,
    isLoading,
    error,
    setError,
    isTimerActive,
    
    // Actions
    fetchNewLog,
    validatePhase,
    validateMitigation,
    
    // Helpers
    phasesCompleted
  }
}