"""
CYBER KILL CHAIN ANALYZER - BACKEND CORRETTO
Versione con bug fix e gestione errori robusta
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime
import json
import logging

# ============================================================================
# INIZIALIZZAZIONE FLASK CON LOGGING
# ============================================================================

app = Flask(__name__)
CORS(app)

# Configurazione logging per debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE CYBER KILL CHAIN
# ============================================================================

CYBER_KILL_CHAIN_PHASES = {
    'reconnaissance': {
        'name': 'Reconnaissance',
        'description': 'L’attaccante raccoglie informazioni sul bersaglio',
        'icon': '🔍'
    },
    'weaponization': {
        'name': 'Weaponization',
        'description': 'Creazione di un payload malevolo unito a un exploit',
        'icon': '🔨'
    },
    'delivery': {
        'name': 'Delivery',
        'description': 'Trasmissione del payload al bersaglio',
        'icon': '📧'
    },
    'exploitation': {
        'name': 'Exploitation',
        'description': 'Attivazione del codice exploit sul sistema vittima',
        'icon': '💥'
    },
    'installation': {
        'name': 'Installation',
        'description': 'Installazione di malware sul sistema bersaglio',
        'icon': '⚙️'
    },
    'command_control': {
        'name': 'Command & Control',
        'description': 'Creazione di un canale per il controllo remoto',
        'icon': '📡'
    },
    'actions_objectives': {
        'name': 'Actions on Objectives',
        'description': 'Raggiungimento degli obiettivi dell’attaccante',
        'icon': '🎯'
    }
}

# Log database
LOGS_DATABASE = {
    'reconnaissance': [
        {
            'id': 'recon_1',
            'raw': '2025-03-15 09:23:17 [IDS] Multiple DNS queries detected from external IP 185.234.218.12 for domain controllers, mail servers, and VPN endpoints. Pattern suggests automated reconnaissance tool usage.',
            'source': 'Network IDS',
            'severity': 'Low',
            'timestamp': '2025-03-15 09:23:17',
            'metadata': {
                'source_ip': '185.234.218.12',
                'queries': 47,
                'targets': ['dc01.company.local', 'mail.company.local', 'vpn.company.local'],
                'tool_signature': 'nmap/dnsrecon'
            },
            'explanation': 'Query DNS multiple verso componenti dell’infrastruttura indicano la fase di ricognizione, in cui gli attaccanti mappano la rete.',
            'phase': 'reconnaissance',
            'indicators': ['Enumerazione DNS', 'Scansione esterna', 'Mappatura dell’infrastruttura']
        }
    ],
    'weaponization': [
        {
            'id': 'weapon_1',
            'raw': '2025-03-16 14:12:45 [Email Security] Suspicious attachment detected: "Invoice_March2025.docm" contains obfuscated VBA macro with PowerShell download cradle. Hash matches known malware builder output.',
            'source': 'Email Security Gateway',
            'severity': 'High',
            'timestamp': '2025-03-16 14:12:45',
            'metadata': {
                'filename': 'Invoice_March2025.docm',
                'file_hash': 'a4b5c6d7e8f9g0h1i2j3',
                'macro_detected': True,
                'payload_type': 'PowerShell downloader'
            },
            'explanation': 'Documento malevolo con macro incorporata rappresenta la fase di weaponization, in cui l’exploit viene confezionato insieme al payload.',
            'phase': 'weaponization',
            'indicators': ['Documento con macro abilitate', 'Codice offuscato', 'Script di download']
        }
    ],
    'delivery': [
        {
            'id': 'delivery_1',
            'raw': '2025-03-17 08:45:12 [Email Gateway] Phishing campaign detected: 47 emails sent to employees from "noreply@companysupport.tk" with subject "Urgent: Update Your Password". Contains link to credential harvesting site.',
            'source': 'Email Security',
            'severity': 'High',
            'timestamp': '2025-03-17 08:45:12',
            'metadata': {
                'sender': 'noreply@companysupport.tk',
                'recipients': 47,
                'subject': 'Urgent: Update Your Password',
                'malicious_url': 'hxxps://company-login[.]tk'
            },
            'explanation': 'Una campagna di phishing di massa rappresenta la fase di delivery, in cui il payload raggiunge i bersagli.',
            'phase': 'delivery',
            'indicators': ['Email di phishing', 'Mittente contraffatto', 'Raccolta di credenziali']
        }
    ],
    'exploitation': [
        {
            'id': 'exploit_1',
            'raw': '2025-03-18 11:15:43 [EDR] Process injection detected: winword.exe spawned powershell.exe with encoded command attempting to bypass AMSI. Memory analysis shows shellcode execution.',
            'source': 'Endpoint Detection',
            'severity': 'Critical',
            'timestamp': '2025-03-18 11:15:43',
            'metadata': {
                'parent_process': 'winword.exe',
                'child_process': 'powershell.exe',
                'technique': 'Process Injection',
                'amsi_bypass': True
            },
            'explanation': 'L’esecuzione di codice malevolo da un documento Word indica l’avvenuta exploitation di una vulnerabilità.',
            'phase': 'exploitation',
            'indicators': ['Iniezione di processo', 'Bypass di AMSI', 'Esecuzione di shellcode']
        }
    ],
    'installation': [
        {
            'id': 'install_1',
            'raw': '2025-03-19 15:23:11 [Sysmon] Registry persistence detected: New service "WindowsUpdateHelper" created pointing to C:\\ProgramData\\update.exe. File signed with invalid certificate, established scheduled task for hourly execution.',
            'source': 'Sysmon',
            'severity': 'High',
            'timestamp': '2025-03-19 15:23:11',
            'metadata': {
                'service_name': 'WindowsUpdateHelper',
                'file_path': 'C:\\ProgramData\\update.exe',
                'persistence_type': 'Service + Scheduled Task',
                'certificate': 'Invalid'
            },
            'explanation': 'Il malware che stabilisce persistenza tramite servizi e attività pianificate indica la fase di installation',
            'phase': 'installation',
            'indicators': ['Creazione di servizio', 'Attività pianificata', 'Meccanismo di persistenza']
        }
    ],
    'command_control': [
        {
            'id': 'c2_1',
            'raw': '2025-03-20 09:12:45 [Network Monitor] Suspicious beaconing detected: Host 10.0.1.45 communicating with 185.234.219.11:443 every 60 seconds with jitter of 10%. Traffic pattern matches Cobalt Strike beacon.',
            'source': 'Network Security Monitor',
            'severity': 'Critical',
            'timestamp': '2025-03-20 09:12:45',
            'metadata': {
                'internal_host': '10.0.1.45',
                'c2_server': '185.234.219.11:443',
                'beacon_interval': '60 seconds',
                'protocol': 'HTTPS'
            },
            'explanation': 'Un pattern regolare di beaconing verso un server esterno indica l’avvenuta creazione di un canale di command and control.',
            'phase': 'command_control',
            'indicators': ['Comportamento di beaconing', 'Intervalli regolari', 'Comunicazione esterna']
        }
    ],
    'actions_objectives': [
        {
            'id': 'action_1',
            'raw': '2025-03-21 14:45:33 [DLP] Mass data exfiltration detected: 15GB of sensitive files from Finance share compressed and uploaded to cloud storage. Files include "Q1_Financial_Report.xlsx", "Customer_Database.csv".',
            'source': 'Data Loss Prevention',
            'severity': 'Critical',
            'timestamp': '2025-03-21 14:45:33',
            'metadata': {
                'data_volume': '15GB',
                'file_types': ['Financial reports', 'Customer data'],
                'destination': 'Cloud storage',
                'compression': True
            },
            'explanation': 'Il furto su larga scala di dati indica che l’attaccante ha raggiunto l’obiettivo di sottrarre informazioni sensibili.',
            'phase': 'actions_objectives',
            'indicators': ['Esfiltrazione di dati', 'File sensibili', 'Grande volume di dati']
        }
    ]
}

# Strategie di mitigazione
MITIGATION_STRATEGIES = {
    'reconnaissance': [
        {
            'id': 'recon_mit_1',
            'name': 'Riduzione della superficie d’attacco',
            'description': 'Limitare i servizi e le informazioni esposte pubblicamente',
            'icon': '🛡️',
            'effectiveness': 'High'
        },
        {
            'id': 'recon_mit_2',
            'name': 'Monitoraggio DNS',
            'description': 'Monitorare e segnalare query DNS sospette',
            'icon': '🔍',
            'effectiveness': 'High'
        }
    ],
    'weaponization': [
        {
            'id': 'weapon_mit_1',
            'name': 'Feed di Threat Intelligence',
            'description': 'Sottoscrivere feed di IOC per rilevare malware noto',
            'icon': '📰',
            'effectiveness': 'High'
        },
        {
            'id': 'weapon_mit_2',
            'name': 'Analisi in sandbox',
            'description': 'Analizzare file sospetti in un ambiente isolato',
            'icon': '📦',
            'effectiveness': 'High'
        }
    ],
    'delivery': [
        {
            'id': 'delivery_mit_1',
            'name': 'Gateway di sicurezza email',
            'description': 'Filtrare email e allegati malevoli',
            'icon': '📧',
            'effectiveness': 'High'
        },
        {
            'id': 'delivery_mit_2',
            'name': 'Whitelist delle applicazioni',
            'description': 'Consentire l’esecuzione solo ad applicazioni approvate',
            'icon': '✅',
            'effectiveness': 'Very High'
        }
    ],
    'exploitation': [
        {
            'id': 'exploit_mit_1',
            'name': 'Gestione delle patch',
            'description': 'Applicare immediatamente le patch di sicurezza',
            'icon': '🔄',
            'effectiveness': 'Very High'
        },
        {
            'id': 'exploit_mit_2',
            'name': 'Soluzione EDR (Endpoint Detection & Response)',
            'description': 'Implementare soluzioni di rilevamento e risposta sugli endpoint (EDR)',
            'icon': '💻',
            'effectiveness': 'High'
        }
    ],
    'installation': [
        {
            'id': 'install_mit_1',
            'name': 'Controllo delle applicazioni',
            'description': 'Impedire l’installazione di software non autorizzato',
            'icon': '🚫',
            'effectiveness': 'Very High'
        },
        {
            'id': 'install_mit_2',
            'name': 'Monitoraggio dell’integrità dei file',
            'description': 'Rilevare modifiche non autorizzate ai file di sistema',
            'icon': '📁',
            'effectiveness': 'High'
        }
    ],
    'command_control': [
        {
            'id': 'c2_mit_1',
            'name': 'Analisi del traffico di rete',
            'description': 'Rilevare connessioni in uscita anomale',
            'icon': '📡',
            'effectiveness': 'High'
        },
        {
            'id': 'c2_mit_2',
            'name': 'DNS Sinkholing',
            'description': 'Reindirizzare i domini malevoli verso un server interno',
            'icon': '🕳️',
            'effectiveness': 'High'
        }
    ],
    'actions_objectives': [
        {
            'id': 'action_mit_1',
            'name': 'Backup e ripristino dei dati',
            'description': 'Mantenere backup offline per il ripristino da ransomware',
            'icon': '💾',
            'effectiveness': 'Very High'
        },
        {
            'id': 'action_mit_2',
            'name': 'Soluzioni DLP (Data Loss Prevention)',
            'description': 'Impedire l’esfiltrazione non autorizzata di dati',
            'icon': '🔒',
            'effectiveness': 'High'
        }
    ]
}

# ============================================================================
# GESTIONE SESSIONI MIGLIORATA
# ============================================================================

user_sessions = {}

def get_or_create_session(session_id):
    """Crea o recupera una sessione utente con valori di default"""
    if session_id not in user_sessions:
        user_sessions[session_id] = {
            'score': 0,
            'streak': 0,
            'total_attempts': 0,
            'correct_attempts': 0,
            'current_log': None,
            'correct_phase': None,
            'correct_mitigation': None,
            'log_data': {}
        }
    return user_sessions[session_id]

# ============================================================================
# FUNZIONI HELPER CON VALIDAZIONE
# ============================================================================

def calculate_difficulty(score, streak, accuracy):
    """Calcola difficoltà basata sulle performance con validazione"""
    try:
        performance_score = (score * 0.3) + (streak * 10) + (accuracy * 0.4)
        
        if performance_score < 50:
            return 'beginner'
        elif performance_score < 150:
            return 'intermediate'
        else:
            return 'expert'
    except (TypeError, ValueError):
        return 'beginner'  # Default sicuro

def get_random_log(difficulty='all'):
    """Ottiene un log casuale dal database con validazione"""
    try:
        if difficulty == 'beginner':
            phases = ['reconnaissance', 'weaponization', 'delivery']
        elif difficulty == 'intermediate':
            phases = ['reconnaissance', 'weaponization', 'delivery', 'exploitation', 'installation']
        else:
            phases = list(LOGS_DATABASE.keys())
        
        # Verifica che ci siano fasi disponibili
        available_phases = [p for p in phases if p in LOGS_DATABASE and LOGS_DATABASE[p]]
        
        if not available_phases:
            # Fallback a reconnaissance se non ci sono fasi disponibili
            selected_phase = 'reconnaissance'
        else:
            selected_phase = random.choice(available_phases)
        
        if selected_phase in LOGS_DATABASE and LOGS_DATABASE[selected_phase]:
            selected_log = random.choice(LOGS_DATABASE[selected_phase])
            return selected_log, selected_phase
        else:
            # Fallback con log di test
            return {
                'id': 'fallback_1',
                'raw': 'Log di test: Rilevate query DNS provenienti da una sorgente esterna verso l’infrastruttura interna.',
                'source': 'Test System',
                'severity': 'Medium',
                'timestamp': datetime.now().isoformat(),
                'metadata': {'test': True}
            }, 'reconnaissance'
            
    except Exception as e:
        logger.error(f"Error in get_random_log: {e}")
        # Fallback sicuro
        return {
            'id': 'error_fallback',
            'raw': 'Log di test generato dal sistema per scopi di addestramento.',
            'source': 'Training System',
            'severity': 'Low',
            'timestamp': datetime.now().isoformat(),
            'metadata': {}
        }, 'reconnaissance'

def calculate_points(difficulty, time_remaining, phase_correct, mitigation_correct):
    """Calcola i punti guadagnati con validazione"""
    try:
        base_points = {
            'beginner': 10,
            'intermediate': 25,
            'expert': 50
        }
        
        points = 0
        
        if phase_correct:
            points += base_points.get(difficulty, 10)
            
            if mitigation_correct:
                points += base_points.get(difficulty, 10)
                time_bonus = max(0, int(time_remaining * 0.5))
                points += time_bonus
        
        return max(0, points)  # Assicura che i punti non siano negativi
        
    except (TypeError, ValueError):
        return 0

# ============================================================================
# ENDPOINTS API CON GESTIONE ERRORI ROBUSTA
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint con informazioni di sistema"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'game': 'Cyber Kill Chain Analyzer',
            'version': '1.0.1',
            'active_sessions': len(user_sessions)
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({'error': 'Health check failed'}), 500

@app.route('/api/get-phases', methods=['GET'])
def get_phases():
    """Ottiene tutte le fasi della Cyber Kill Chain"""
    try:
        phases = []
        for key, value in CYBER_KILL_CHAIN_PHASES.items():
            phases.append({
                'id': key,
                'name': value['name'],
                'description': value['description'],
                'icon': value['icon']
            })
        return jsonify({'phases': phases})
    except Exception as e:
        logger.error(f"Error in get_phases: {e}")
        return jsonify({'error': 'Failed to get phases'}), 500

@app.route('/api/get-log', methods=['POST'])
def get_log():
    """Ottiene un nuovo log da analizzare con gestione errori"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        session_id = data.get('session_id', 'default')
        difficulty = data.get('difficulty', 'beginner')
        stats = data.get('stats', {})
        
        # Valida difficulty
        if difficulty not in ['beginner', 'intermediate', 'expert']:
            difficulty = 'beginner'
        
        # Ottiene o crea sessione
        session = get_or_create_session(session_id)
        
        # Seleziona un log casuale
        selected_log, selected_phase = get_random_log(difficulty)
        
        # Salva la risposta corretta in sessione
        session['current_log'] = selected_log['id']
        session['correct_phase'] = selected_phase
        session['log_data'] = selected_log
        
        # Prepara il log per il client (senza la soluzione)
        response_log = {
            'id': selected_log['id'],
            'raw': selected_log['raw'],
            'source': selected_log['source'],
            'severity': selected_log['severity'],
            'timestamp': selected_log['timestamp'],
            'metadata': selected_log.get('metadata', {})
        }
        
        # Tempo limite basato sulla difficoltà
        time_limits = {
            'beginner': 70,
            'intermediate': 60,
            'expert': 45
        }
        
        logger.info(f"Generated log {selected_log['id']} for session {session_id} at difficulty {difficulty}")
        
        return jsonify({
            'log': response_log,
            'time_limit': time_limits.get(difficulty, 60)
        })
        
    except Exception as e:
        logger.error(f"Error in get_log: {e}")
        return jsonify({'error': 'Failed to generate log'}), 500

@app.route('/api/validate-phase', methods=['POST'])
def validate_phase():
    """Valida la fase selezionata dall'utente con gestione errori"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        session_id = data.get('session_id', 'default')
        selected_phase = data.get('selected_phase')
        
        if not selected_phase:
            return jsonify({'error': 'No phase selected'}), 400
        
        # Verifica che la fase selezionata sia valida
        if selected_phase not in CYBER_KILL_CHAIN_PHASES:
            return jsonify({'error': 'Invalid phase selected'}), 400
        
        session = get_or_create_session(session_id)
        correct_phase = session.get('correct_phase')
        log_data = session.get('log_data', {})
        
        if not correct_phase:
            return jsonify({'error': 'No active log to validate'}), 400
        
        is_correct = selected_phase == correct_phase
        
        if is_correct:
            # Se corretto, prepara le strategie di mitigazione
            mitigation_options = MITIGATION_STRATEGIES.get(correct_phase, [])
            
            # Salva la mitigazione corretta in sessione
            if mitigation_options:
                correct_mitigation = random.choice([m for m in mitigation_options if m['effectiveness'] in ['High', 'Very High']])
                session['correct_mitigation'] = correct_mitigation['id']
            
            logger.info(f"Correct phase {selected_phase} selected by session {session_id}")
            
            return jsonify({
                'is_correct': True,
                'mitigation_strategies': mitigation_options,
                'explanation': log_data.get('explanation', ''),
                'indicators': log_data.get('indicators', [])
            })
        else:
            logger.info(f"Incorrect phase {selected_phase} selected by session {session_id}, correct was {correct_phase}")
            
            return jsonify({
                'is_correct': False,
                'correct_phase': correct_phase,
                'phase_info': CYBER_KILL_CHAIN_PHASES.get(correct_phase, {}),
                'explanation': log_data.get('explanation', ''),
                'indicators': log_data.get('indicators', [])
            })
            
    except Exception as e:
        logger.error(f"Error in validate_phase: {e}")
        return jsonify({'error': 'Failed to validate phase'}), 500

@app.route('/api/validate-mitigation', methods=['POST'])
def validate_mitigation():
    """Valida la strategia di mitigazione selezionata con gestione errori"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        session_id = data.get('session_id', 'default')
        selected_mitigation = data.get('selected_mitigation')
        time_remaining = data.get('time_remaining', 0)
        difficulty = data.get('difficulty', 'beginner')
        
        if not selected_mitigation:
            return jsonify({'error': 'No mitigation selected'}), 400
        
        session = get_or_create_session(session_id)
        correct_mitigation = session.get('correct_mitigation')
        correct_phase = session.get('correct_phase')
        
        if not correct_phase:
            return jsonify({'error': 'No active phase to validate mitigation'}), 400
        
        # Verifica se la mitigazione è appropriata
        phase_mitigations = MITIGATION_STRATEGIES.get(correct_phase, [])
        selected_mit_data = next((m for m in phase_mitigations if m['id'] == selected_mitigation), None)
        
        if not selected_mit_data:
            return jsonify({'error': 'Invalid mitigation selected'}), 400
        
        # Considera corretta se l'efficacia è High o Very High
        is_correct = selected_mit_data['effectiveness'] in ['High', 'Very High']
        
        # Calcola punti
        points = calculate_points(difficulty, time_remaining, True, is_correct)
        
        # Trova la mitigazione migliore
        best_mitigation = next((m for m in phase_mitigations if m['id'] == correct_mitigation), None)
        
        logger.info(f"Mitigation {selected_mitigation} ({'correct' if is_correct else 'incorrect'}) selected by session {session_id}")
        
        return jsonify({
            'is_correct': is_correct,
            'points': points,
            'selected_effectiveness': selected_mit_data['effectiveness'],
            'best_mitigation': best_mitigation
        })
        
    except Exception as e:
        logger.error(f"Error in validate_mitigation: {e}")
        return jsonify({'error': 'Failed to validate mitigation'}), 500

@app.route('/api/statistics', methods=['POST'])
def get_statistics():
    """Ottiene statistiche dell'utente"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default') if data else 'default'
        
        session = get_or_create_session(session_id)
        
        stats = {
            'total_games': session.get('total_attempts', 0),
            'correct_answers': session.get('correct_attempts', 0),
            'current_score': session.get('score', 0),
            'current_streak': session.get('streak', 0),
            'accuracy': round((session.get('correct_attempts', 0) / max(1, session.get('total_attempts', 1))) * 100, 2)
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error in get_statistics: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Ottiene la classifica globale (mock data)"""
    try:
        leaderboard = [
            {'rank': 1, 'name': 'CyberHunter', 'score': 2150, 'mastery': '7/7 phases'},
            {'rank': 2, 'name': 'SecurityPro', 'score': 1890, 'mastery': '6/7 phases'},
            {'rank': 3, 'name': 'KillChainMaster', 'score': 1750, 'mastery': '7/7 phases'},
            {'rank': 4, 'name': 'ThreatAnalyst', 'score': 1620, 'mastery': '5/7 phases'},
            {'rank': 5, 'name': 'BlueTeamer', 'score': 1500, 'mastery': '4/7 phases'}
        ]
        
        return jsonify({'leaderboard': leaderboard})
        
    except Exception as e:
        logger.error(f"Error in get_leaderboard: {e}")
        return jsonify({'error': 'Failed to get leaderboard'}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    logger.info("Starting Cyber Kill Chain Analyzer Backend...")
    app.run(debug=True, port=5000, host='127.0.0.1')