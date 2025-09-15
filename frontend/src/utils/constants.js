/**
 * CYBER KILL CHAIN ANALYZER - COSTANTI E CONFIGURAZIONE
 * Questo file contiene tutte le costanti, dati statici e configurazioni 
 * utilizzate dall'applicazione frontend
 */

// ============================================================================
// CONFIGURAZIONE DELL'API E CONNESSIONE BACKEND
// ============================================================================

// URL dell'API backend - usa variabile d'ambiente se disponibile, altrimenti localhost
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

// ID univoco della sessione generato casualmente per identificare l'utente
// Formato: 'user_' + stringa casuale di 9 caratteri
export const SESSION_ID = 'user_' + Math.random().toString(36).substr(2, 9)

// Timeout per le richieste API in millisecondi (10 secondi)
// Aumentato per gestire il rate limiting del backend
export const API_TIMEOUT = 10000

// ============================================================================
// DATI DELLE FASI DELLA CYBER KILL CHAIN
// Basato sul framework di Lockheed Martin per la cybersecurity education
// ============================================================================

export const KILL_CHAIN_PHASES = [
  {
    id: 'reconnaissance',           // ID univoco per la fase
    name: 'Ricognizione',          // Nome tradotto in italiano
    icon: '🔍',                    // Emoji per l'interfaccia
    description: 'Raccolta informazioni sul bersaglio',  // Descrizione italiana fluida
    color: '#3b82f6'              
  },
  {
    id: 'weaponization',
    name: 'Armamento', 
    icon: '🔨',
    description: 'Creazione del carico dannoso',
    color: '#8b5cf6'              
  },
  {
    id: 'delivery',
    name: 'Consegna',
    icon: '📧', 
    description: 'Invio del malware al bersaglio',
    color: '#ec4899'              
  },
  {
    id: 'exploitation',
    name: 'Sfruttamento',
    icon: '💥',
    description: 'Esecuzione dell\'exploit sui sistemi', 
    color: '#f59e0b'              
  },
  {
    id: 'installation',
    name: 'Installazione',
    icon: '⚙️',
    description: 'Installazione permanente del malware',
    color: '#10b981'              
  },
  {
    id: 'command_control',
    name: 'Comando e Controllo',
    icon: '📡',
    description: 'Controllo remoto del sistema compromesso',
    color: '#06b6d4'              
  },
  {
    id: 'actions_objectives',
    name: 'Azioni sugli Obiettivi',
    icon: '🎯',
    description: 'Realizzazione degli scopi dell\'attacco',
    color: '#ef4444'              
  }
]

// ============================================================================
// DATI DI FALLBACK PER MODALITÀ OFFLINE
// Usati quando il backend non è disponibile per mantenere l'esperienza educativa
// ============================================================================

// Log di sicurezza di esempio per diverse fasi della kill chain
export const FALLBACK_LOGS = [
  {
    id: 'fallback_recon',
    raw: 'Multiple DNS queries detected from external IP 185.234.218.12 for domain controllers and mail servers. Pattern suggests automated reconnaissance.',
    source: 'IDS di Rete',                   // Tradotto: Network IDS
    severity: 'Media',                       // Tradotto: Medium
    timestamp: new Date().toISOString(),     // Timestamp corrente
    metadata: {                              // Dati aggiuntivi strutturati
      source_ip: '185.234.218.12',
      queries: 47,
      targets: ['dc01.company.local', 'mail.company.local']
    }
  },
  {
    id: 'fallback_delivery',
    raw: 'Phishing campaign detected: 47 emails sent from "noreply@companysupport.tk" with malicious links to credential harvesting site.',
    source: 'Sicurezza Email',               // Tradotto: Email Security
    severity: 'Alta',                        // Tradotto: High
    timestamp: new Date().toISOString(),
    metadata: {
      sender: 'noreply@companysupport.tk',
      recipients: 47,
      malicious_url: 'company-login.tk'
    }
  },
  {
    id: 'fallback_exploit',
    raw: 'Process injection detected: winword.exe spawned powershell.exe with encoded command attempting to bypass AMSI. Memory analysis shows shellcode execution.',
    source: 'Rilevamento Endpoint',          // Tradotto: Endpoint Detection
    severity: 'Critica',                     // Tradotto: Critical
    timestamp: new Date().toISOString(),
    metadata: {
      parent_process: 'winword.exe',
      child_process: 'powershell.exe',
      technique: 'Process Injection'
    }
  }
]

// Strategie di mitigazione di esempio per la modalità offline
export const FALLBACK_MITIGATIONS = [
  {
    id: 'mit_1',
    name: 'Monitoraggio di Rete',            // Tradotto: Network Monitoring
    description: 'Monitora il traffico di rete per individuare pattern sospetti',
    icon: '📡',
    effectiveness: 'Alta'                    // Tradotto: High
  },
  {
    id: 'mit_2', 
    name: 'Filtro Email',                    // Tradotto: Email Filtering
    description: 'Filtra email dannose e allegati sospetti',
    icon: '📧',
    effectiveness: 'Molto Alta'              // Tradotto: Very High
  },
  {
    id: 'mit_3',
    name: 'Formazione Utenti',               // Tradotto: User Training
    description: 'Addestra gli utenti a riconoscere le minacce di sicurezza',
    icon: '🎓',
    effectiveness: 'Media'                   // Tradotto: Medium
  },
  {
    id: 'mit_4',
    name: 'Rilevamento Endpoint',            // Tradotto: Endpoint Detection
    description: 'Implementa soluzioni EDR per il rilevamento in tempo reale', 
    icon: '💻',
    effectiveness: 'Alta'                    // Tradotto: High
  }
]

// ============================================================================
// SISTEMA DI ACHIEVEMENTS E RICONOSCIMENTI
// Definisce i traguardi che i giocatori possono sbloccare
// ============================================================================

export const ACHIEVEMENT_CONFIG = {
  streak_5: {
    name: 'In Fiamme! 🔥',                   // Tradotto: On Fire!
    description: 'Raggiungi una serie di 5 risposte corrette consecutive',
    icon: '🔥'
  },
  streak_10: {
    name: 'Inarrestabile! ⚡',               // Tradotto: Unstoppable!
    description: 'Raggiungi una serie di 10 risposte corrette consecutive',
    icon: '⚡'
  },
  score_500: {
    name: 'Difensore Cyber 🛡️',             // Tradotto: Cyber Defender
    description: 'Raggiungi un punteggio totale di 500 punti', 
    icon: '🛡️'
  },
  score_1000: {
    name: 'Maestro della Kill Chain 👑',     // Tradotto: Kill Chain Master
    description: 'Raggiungi un punteggio totale di 1000 punti',
    icon: '👑'
  },
  phase_master: {
    name: 'Esperto di Fasi 🎯',              // Tradotto: Phase Expert
    description: 'Completa con successo almeno 3 volte 4 fasi diverse',
    icon: '🎯'
  }
}

// ============================================================================
// CONFIGURAZIONE LIVELLI DI DIFFICOLTÀ
// Definisce i parametri per ogni livello di difficoltà del gioco
// ============================================================================

export const DIFFICULTY_CONFIG = {
  beginner: {
    name: 'Principiante',                    // Già tradotto correttamente
    phases: 3,                              // Solo le prime 3 fasi della kill chain
    timeLimit: 60,                          // 60 secondi per rispondere
    basePoints: 10                          // Punti base per risposta corretta
  },
  intermediate: {
    name: 'Intermedio',                      // Già tradotto correttamente
    phases: 5,                              // Prime 5 fasi della kill chain
    timeLimit: 40,                          // 40 secondi per rispondere
    basePoints: 25                          // Più punti per maggiore difficoltà
  },
  expert: {
    name: 'Esperto',                         // Già tradotto correttamente
    phases: 7,                              // Tutte e 7 le fasi
    timeLimit: 30,                          // Solo 30 secondi per rispondere
    basePoints: 50                          // Massimo punteggio per esperti
  }
}

// ============================================================================
// COSTANTI PER L'INTERFACCIA UTENTE
// ============================================================================

// Stati del timer per cambiare colori e animazioni
export const TIMER_STATES = {
  NORMAL: 'normal',         // Tempo normale (verde/blu)
  WARNING: 'warning',       // Avvertimento <= 30 secondi (arancione)
  CRITICAL: 'critical'      // Critico <= 15 secondi (rosso lampeggiante)
}

// Tipi di feedback che possono essere mostrati al giocatore
export const FEEDBACK_TYPES = {
  PHASE_CORRECT: 'phase_correct',       // Fase identificata correttamente
  PHASE_INCORRECT: 'phase_incorrect',   // Fase identificata male  
  TIMEOUT: 'timeout',                   // Tempo scaduto
  FINAL: 'final'                       // Feedback finale dopo mitigazione
}

// Stati principali del gioco che determinano quale schermata mostrare
export const GAME_STATES = {
  WELCOME: 'welcome',                   // Schermata di benvenuto iniziale
  TUTORIAL: 'tutorial',                 // Schermata tutorial/istruzioni
  PLAYING: 'playing',                   // Gioco attivo - analisi log
  MITIGATION: 'mitigation',             // Selezione strategia di mitigazione  
  PHASE_FEEDBACK: 'phase_feedback',     // Feedback dopo selezione fase
  FINAL_FEEDBACK: 'final_feedback'      // Feedback finale dopo mitigazione
}