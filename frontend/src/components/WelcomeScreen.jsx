/**
 * WELCOME SCREEN COMPONENT
 * 
 * Questo componente gestisce due schermate principali:
 * 1. Schermata di benvenuto con preview del gioco
 * 2. Schermata tutorial con istruzioni dettagliate
 * 
 * È il primo punto di contatto dell'utente con l'applicazione
 */

import { KILL_CHAIN_PHASES, GAME_STATES } from '../utils/constants.js'

export function WelcomeScreen({ 
  gameState,                // Stato corrente (welcome o tutorial)
  setGameState,            // Funzione per cambiare stato
  fetchNewLog,             // Funzione per iniziare il gioco  
  isLoading,               // Se sta caricando dati
  isBackendAvailable       // Se il backend è raggiungibile
}) {

  // ========================================
  // SCHERMATA TUTORIAL
  // Mostra istruzioni dettagliate su come giocare
  // ========================================

  if (gameState === GAME_STATES.TUTORIAL) {
    return (
      <div className="tutorial-screen">
        <div className="tutorial-content">
          
          {/* Header del tutorial con titolo e sottotitolo */}
          <div className="tutorial-header">
            <h1>📖 Come Giocare</h1>
            <p>Impara a identificare e bloccare gli attacchi informatici!</p>
          </div>

          {/* Griglia con i passaggi del tutorial */}
          <div className="tutorial-steps">
            
            {/* STEP 1: Analisi del Log */}
            <div className="tutorial-step">
              <span className="step-number">1</span>
              <div className="step-content">
                <h3>📋 Analizza il Log</h3>
                <p>
                  In ogni round ti verrà presentato un log di sicurezza reale. 
                  Leggilo attentamente per identificare gli indicatori di attacco.
                </p>
              </div>
            </div>

            {/* STEP 2: Identificazione della Fase */}
            <div className="tutorial-step">
              <span className="step-number">2</span>
              <div className="step-content">
                <h3>🎯 Identifica la Fase</h3>
                <p>
                  Basandoti sugli indicatori nel log, determina in quale delle 7 fasi 
                  della Cyber Kill Chain si trova l'attaccante.
                </p>
              </div>
            </div>

            {/* STEP 3: Selezione della Mitigazione */}
            <div className="tutorial-step">
              <span className="step-number">3</span>
              <div className="step-content">
                <h3>🛡️ Scegli la Contromisura</h3>
                <p>
                  Se identifichi correttamente la fase, dovrai scegliere la strategia 
                  di difesa più efficace per interrompere l'attacco.
                </p>
              </div>
            </div>

            {/* STEP 4: Sistema di Punteggio */}
            <div className="tutorial-step">
              <span className="step-number">4</span>
              <div className="step-content">
                <h3>⏱️ Tempo e Punti</h3>
                <p>
                  Più rapidamente rispondi correttamente, più punti guadagni! 
                  Il timer si adatta alle tue competenze crescenti.
                </p>
              </div>
            </div>
            
          </div>

          {/* Pulsante per tornare alla schermata principale */}
          <button 
            className="btn-start-game" 
            onClick={() => setGameState(GAME_STATES.WELCOME)}
          >
            Ho Capito! Iniziamo 🚀
          </button>
          
        </div>
      </div>
    )
  }

  // ========================================
  // SCHERMATA DI BENVENUTO PRINCIPALE
  // Prima schermata che vedono gli utenti
  // ========================================

  return (
    <div className="welcome-screen">
      <div className="welcome-content">
        
        {/* Logo e branding dell'applicazione */}
        <div className="logo-container">
          <div className="logo-circle">
            <span className="logo-icon">🛡️</span>
          </div>
          <div className="logo-text">Cyber Kill Chain</div>
          <div className="logo-subtitle">Analyzer</div>
        </div>

        {/* Descrizione dell'applicazione educativa */}
        <p className="welcome-description">
          Impara a identificare e interrompere gli attacchi informatici
          analizzando log di sicurezza reali attraverso le 7 fasi della Cyber Kill Chain
        </p>

        {/* Avviso modalità offline se backend non disponibile */}
        {!isBackendAvailable && (
          <div className="offline-notice">
            <span className="offline-icon">📡</span>
            <span>Modalità Offline Attiva - Funzionalità Limitate</span>
          </div>
        )}

        {/* Preview delle 7 fasi della Kill Chain */}
        <div className="kill-chain-preview">
          {KILL_CHAIN_PHASES.map((phase, index) => (
            <div key={phase.id} className="preview-phase">
              {/* Numero della fase (1-7) */}
              <span className="phase-number">{index + 1}</span>
              {/* Icona rappresentativa */}
              <span className="phase-icon">{phase.icon}</span>
              {/* Nome della fase */}
              <span className="phase-name">{phase.name}</span>
            </div>
          ))}
        </div>

        {/* Pulsanti di azione principali */}
        <div className="welcome-buttons">
          
          {/* Pulsante principale per iniziare a giocare */}
          <button
            className="btn-primary"
            onClick={fetchNewLog}        // Avvia direttamente il gioco
            disabled={isLoading}        // Disabilita durante caricamento
          >
            {isLoading ? '⏳ Caricamento...' : '🎮 Inizia a Giocare'}
          </button>
          
          {/* Pulsante secondario per vedere le istruzioni */}
          <button 
            className="btn-secondary" 
            onClick={() => setGameState(GAME_STATES.TUTORIAL)}
          >
            📖 Come Giocare
          </button>
          
        </div>
        
      </div>
    </div>
  )
}