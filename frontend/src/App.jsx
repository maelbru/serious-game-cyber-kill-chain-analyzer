/**
 * CYBER KILL CHAIN ANALYZER - MAIN APP 
 * Versione pulita con componenti separati
 */

import './App.css'
import { useGameLogic } from './hooks/useGameLogic.js'
import { WelcomeScreen } from './components/WelcomeScreen.jsx'
import { GameScreen } from './components/GameScreen.jsx'
import { FeedbackModals } from './components/FeedbackModals.jsx'
import { GAME_STATES } from './utils/constants.js'

// ============================================================================
// ERROR BANNER COMPONENT
// ============================================================================

function ErrorBanner({ error, onClose }) {
  if (!error) return null

  return (
    <div className="error-banner" onClick={onClose}>
      <span className="error-icon">⚠️</span>
      <span className="error-message">{error}</span>
      <span className="error-close">✕</span>
    </div>
  )
}

// ============================================================================
// MAIN APP COMPONENT
// ============================================================================

function App() {
  // Custom hook che gestisce tutta la business logic
  const gameLogic = useGameLogic()

  // ========================================
  // ROUTING BASED ON GAME STATE
  // ========================================

  return (
    <>
      {/* Error Banner - sempre visibile quando presente */}
      <ErrorBanner 
        error={gameLogic.error} 
        onClose={() => gameLogic.setError(null)} 
      />

      {/* Welcome/Tutorial Screens */}
      {(gameLogic.gameState === GAME_STATES.WELCOME || 
        gameLogic.gameState === GAME_STATES.TUTORIAL) && (
        <WelcomeScreen
          gameState={gameLogic.gameState}
          setGameState={gameLogic.setGameState}
          fetchNewLog={gameLogic.fetchNewLog}
          isLoading={gameLogic.isLoading}
          isBackendAvailable={gameLogic.isBackendAvailable}
        />
      )}

      {/* Game Screens (Playing + Mitigation) */}
      {(gameLogic.gameState === GAME_STATES.PLAYING || 
        gameLogic.gameState === GAME_STATES.MITIGATION) && (
        <GameScreen
          // Game State
          gameState={gameLogic.gameState}
          difficulty={gameLogic.difficulty}
          isBackendAvailable={gameLogic.isBackendAvailable}
          
          // Player Stats
          score={gameLogic.score}
          streak={gameLogic.streak}
          level={gameLogic.level}
          accuracy={gameLogic.accuracy}
          
          // Current Round
          currentLog={gameLogic.currentLog}
          timeRemaining={gameLogic.timeRemaining}
          selectedPhase={gameLogic.selectedPhase}
          setSelectedPhase={gameLogic.setSelectedPhase}
          selectedMitigation={gameLogic.selectedMitigation}
          setSelectedMitigation={gameLogic.setSelectedMitigation}
          mitigationStrategies={gameLogic.mitigationStrategies}
          
          // UI State
          isLoading={gameLogic.isLoading}
          
          // Actions
          validatePhase={gameLogic.validatePhase}
          validateMitigation={gameLogic.validateMitigation}
        />
      )}

      {/* Feedback Modals - sempre renderizzato per gestire overlay */}
      <FeedbackModals
        gameState={gameLogic.gameState}
        feedback={gameLogic.feedback}
        fetchNewLog={gameLogic.fetchNewLog}
        isLoading={gameLogic.isLoading}
        score={gameLogic.score}
        accuracy={gameLogic.accuracy}
        level={gameLogic.level}
      />
    </>
  )
}

export default App