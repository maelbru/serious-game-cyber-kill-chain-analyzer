/**
 * CYBER KILL CHAIN ANALYZER - CONSTANTS
 * Tutte le costanti e dati statici del gioco
 */

// ============================================================================
// CONFIGURAZIONE API
// ============================================================================

export const API_URL = 'http://localhost:5000/api'
export const SESSION_ID = 'user_' + Math.random().toString(36).substr(2, 9)
export const API_TIMEOUT = 5000

// ============================================================================
// KILL CHAIN PHASES DATA
// ============================================================================

export const KILL_CHAIN_PHASES = [
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
// FALLBACK DATA (MODALITÀ OFFLINE)
// ============================================================================

export const FALLBACK_LOGS = [
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

export const FALLBACK_MITIGATIONS = [
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
// ACHIEVEMENTS DATA
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
// DIFFICULTY SETTINGS
// ============================================================================

export const DIFFICULTY_CONFIG = {
  beginner: {
    name: 'Principiante',
    phases: 3, // Solo prime 3 fasi
    timeLimit: 60,
    basePoints: 10
  },
  intermediate: {
    name: 'Intermedio',
    phases: 5, // Prime 5 fasi
    timeLimit: 40,
    basePoints: 25
  },
  expert: {
    name: 'Esperto',
    phases: 7, // Tutte le fasi
    timeLimit: 30,
    basePoints: 50
  }
}

// ============================================================================
// UI CONSTANTS
// ============================================================================

export const TIMER_STATES = {
  NORMAL: 'normal',
  WARNING: 'warning', // <= 30 secondi
  CRITICAL: 'critical' // <= 15 secondi
}

export const FEEDBACK_TYPES = {
  PHASE_CORRECT: 'phase_correct',
  PHASE_INCORRECT: 'phase_incorrect',
  TIMEOUT: 'timeout',
  FINAL: 'final'
}

export const GAME_STATES = {
  WELCOME: 'welcome',
  TUTORIAL: 'tutorial',
  PLAYING: 'playing',
  MITIGATION: 'mitigation',
  PHASE_FEEDBACK: 'phase_feedback',
  FINAL_FEEDBACK: 'final_feedback'
}