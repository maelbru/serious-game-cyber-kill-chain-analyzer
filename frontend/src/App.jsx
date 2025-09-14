/**
 * CYBER KILL CHAIN ANALYZER - COMPONENTE PRINCIPALE
 * Questo è il componente radice dell'applicazione React
 */

// Importa gli stili CSS personalizzati
import './App.css'

// Importa il custom hook che gestisce tutta la logica del gioco
import { useGameLogic } from './hooks/useGameLogic.js'

// Importa i componenti dell'interfaccia utente
import { WelcomeScreen } from './components/WelcomeScreen.jsx'
import { GameScreen } from './components/GameScreen.jsx'
import { FeedbackModals } from './components/FeedbackModals.jsx'

// Importa le costanti per gli stati del gioco
import { GAME_STATES } from './utils/constants.js'

// ============================================================================
// COMPONENTE ERROR BANNER
// Banner che mostra errori in modo non invasivo nell'angolo dello schermo
// ============================================================================

function ErrorBanner({ error, onClose }) {
  // Non renderizzare nulla se non c'è nessun errore da mostrare
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
// COMPONENTE PRINCIPALE DELL'APPLICAZIONE
// Coordina tutti i sotto-componenti e gestisce il routing basato sullo stato
// ============================================================================

function App() {
  // Il custom hook useGameLogic incapsula tutta la business logic:
  // - Gestione dello stato del gioco
  // - Comunicazioni con il backend
  // - Calcolo di punteggi e statistiche  
  // - Timer e logica delle sessioni
  const gameLogic = useGameLogic()

  // ========================================
  // ROUTING BASATO SULLO STATO DEL GIOCO
  // Invece di usare React Router, usiamo il game state per determinare 
  // quale schermata mostrare. Questo rende l'app più semplice e prevedibile.
  // ========================================

  return (
    <>
      {/* 
        ERROR BANNER - sempre visibile quando c'è un errore
        Posizionato fisso nell'angolo per non interferire con l'UI principale 
      */}
      <ErrorBanner 
        error={gameLogic.error} 
        onClose={() => gameLogic.setError(null)} 
      />

      {/* 
        SCHERMATE DI BENVENUTO E TUTORIAL
        Mostrate quando l'utente non ha ancora iniziato a giocare
      */}
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

      {/* 
        SCHERMATE DI GIOCO ATTIVO
        Include sia la schermata di analisi dei log che quella di selezione mitigazioni
      */}
      {(gameLogic.gameState === GAME_STATES.PLAYING || 
        gameLogic.gameState === GAME_STATES.MITIGATION) && (
        <GameScreen
          // Stato generale del gioco
          gameState={gameLogic.gameState}
          difficulty={gameLogic.difficulty}
          isBackendAvailable={gameLogic.isBackendAvailable}
          
          // Statistiche e progressi del giocatore
          score={gameLogic.score}
          streak={gameLogic.streak}
          level={gameLogic.level}
          accuracy={gameLogic.accuracy}
          
          // Dati del round corrente
          currentLog={gameLogic.currentLog}
          timeRemaining={gameLogic.timeRemaining}
          selectedPhase={gameLogic.selectedPhase}
          setSelectedPhase={gameLogic.setSelectedPhase}
          selectedMitigation={gameLogic.selectedMitigation}
          setSelectedMitigation={gameLogic.setSelectedMitigation}
          mitigationStrategies={gameLogic.mitigationStrategies}
          
          // Stato dell'interfaccia utente
          isLoading={gameLogic.isLoading}
          
          // Funzioni di azione (callback)
          validatePhase={gameLogic.validatePhase}
          validateMitigation={gameLogic.validateMitigation}
        />
      )}

      {/* 
        MODALI DI FEEDBACK
        Sempre renderizzati per gestire gli overlay quando necessario.
        Il componente stesso decide quando mostrarsi basandosi sul game state.
      */}
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

// Esporta il componente come default export
export default App