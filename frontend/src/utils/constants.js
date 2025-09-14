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
    name: 'Reconnaissance',         // Nome user-friendly
    icon: '🔍',                    // Emoji per l'interfaccia
    description: 'Raccolta informazioni sul target',  // Spiegazione educativa
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
// DATI DI FALLBACK PER MODALITÀ OFFLINE
// Usati quando il backend non è disponibile per mantenere l'esperienza educativa
// ============================================================================

// Log di sicurezza di esempio per diverse fasi della kill chain
export const FALLBACK_LOGS = [
  {
    id: 'fallback_recon',
    raw: 'Multiple DNS queries detected from external IP 185.234.218.12 for domain controllers and mail servers. Pattern suggests automated reconnaissance.',
    source: 'Network IDS',                    // Sistema che ha generato il log
    severity: 'Medium',                       // Livello di gravità
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
    source: 'Email Security',
    severity: 'High',
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
    source: 'Endpoint Detection',
    severity: 'Critical',
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
    name: 'Network Monitoring',
    description: 'Monitor network traffic for suspicious patterns',
    icon: '📡',
    effectiveness: 'High'              // Livello di efficacia della strategia
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
  },
  {
    id: 'mit_4',
    name: 'Endpoint Detection',
    description: 'Deploy EDR solutions for real-time threat detection', 
    icon: '💻',
    effectiveness: 'High'
  }
]

// ============================================================================
// SISTEMA DI ACHIEVEMENTS E RICONOSCIMENTI
// Definisce i traguardi che i giocatori possono sbloccare
// ============================================================================

export const ACHIEVEMENT_CONFIG = {
  streak_5: {
    name: 'On Fire! 🔥',
    description: 'Raggiungi una streak di 5 risposte corrette',
    icon: '🔥'
  },
  streak_10: {
    name: 'Unstoppable! ⚡', 
    description: 'Raggiungi una streak di 10 risposte corrette',
    icon: '⚡'
  },
  score_500: {
    name: 'Cyber Defender 🛡️',
    description: 'Raggiungi 500 punti totali', 
    icon: '🛡️'
  },
  score_1000: {
    name: 'Kill Chain Master 👑',
    description: 'Raggiungi 1000 punti totali',
    icon: '👑'
  },
  phase_master: {
    name: 'Phase Expert 🎯',
    description: 'Completa almeno 3 volte 4 fasi diverse',
    icon: '🎯'
  }
}

// ============================================================================
// CONFIGURAZIONE LIVELLI DI DIFFICOLTÀ
// Definisce i parametri per ogni livello di difficoltà del gioco
// ============================================================================

export const DIFFICULTY_CONFIG = {
  beginner: {
    name: 'Principiante',
    phases: 3,              // Solo le prime 3 fasi della kill chain
    timeLimit: 60,          // 60 secondi per rispondere
    basePoints: 10          // Punti base per risposta corretta
  },
  intermediate: {
    name: 'Intermedio',
    phases: 5,              // Prime 5 fasi della kill chain
    timeLimit: 40,          // 40 secondi per rispondere
    basePoints: 25          // Più punti per maggiore difficoltà
  },
  expert: {
    name: 'Esperto', 
    phases: 7,              // Tutte e 7 le fasi
    timeLimit: 30,          // Solo 30 secondi per rispondere
    basePoints: 50          // Massimo punteggio per esperti
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