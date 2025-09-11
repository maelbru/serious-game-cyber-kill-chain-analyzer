"""
CYBER KILL CHAIN ANALYZER - BACKEND
Serious game per l'identificazione delle fasi della Cyber Kill Chain
e selezione di strategie di mitigazione appropriate
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime
import json

# ============================================================================
# INIZIALIZZAZIONE FLASK
# ============================================================================

app = Flask(__name__)
CORS(app)

# ============================================================================
# DATABASE CYBER KILL CHAIN
# ============================================================================

"""
Le 7 fasi della Cyber Kill Chain di Lockheed Martin:
1. Reconnaissance - Ricognizione
2. Weaponization - Creazione dell'arma
3. Delivery - Consegna
4. Exploitation - Sfruttamento
5. Installation - Installazione
6. Command & Control - Comando e controllo
7. Actions on Objectives - Azioni sugli obiettivi
"""

CYBER_KILL_CHAIN_PHASES = {
    'reconnaissance': {
        'name': 'Reconnaissance',
        'description': 'Attacker is gathering information about the target',
        'icon': '🔍'
    },
    'weaponization': {
        'name': 'Weaponization',
        'description': 'Creating malicious payload coupled with exploit',
        'icon': '🔨'
    },
    'delivery': {
        'name': 'Delivery',
        'description': 'Transmitting weapon to the target',
        'icon': '📧'
    },
    'exploitation': {
        'name': 'Exploitation',
        'description': 'Triggering exploit code on victim system',
        'icon': '💥'
    },
    'installation': {
        'name': 'Installation',
        'description': 'Installing malware on the target system',
        'icon': '⚙️'
    },
    'command_control': {
        'name': 'Command & Control',
        'description': 'Establishing channel for remote control',
        'icon': '📡'
    },
    'actions_objectives': {
        'name': 'Actions on Objectives',
        'description': 'Achieving the attacker\'s goals',
        'icon': '🎯'
    }
}

# ============================================================================
# DATABASE LOG PER OGNI FASE
# ============================================================================

LOGS_DATABASE = {
    'reconnaissance': [
        {
            'id': 'recon_1',
            'raw': '2024-03-15 09:23:17 [IDS] Multiple DNS queries detected from external IP 185.234.218.12 for domain controllers, mail servers, and VPN endpoints. Pattern suggests automated reconnaissance tool usage.',
            'source': 'Network IDS',
            'severity': 'Low',
            'timestamp': '2024-03-15 09:23:17',
            'metadata': {
                'source_ip': '185.234.218.12',
                'queries': 47,
                'targets': ['dc01.company.local', 'mail.company.local', 'vpn.company.local'],
                'tool_signature': 'nmap/dnsrecon'
            },
            'explanation': 'Multiple DNS queries for infrastructure components indicate reconnaissance phase where attackers map the network.',
            'phase': 'reconnaissance',
            'indicators': ['DNS enumeration', 'External scanning', 'Infrastructure mapping']
        },
        {
            'id': 'recon_2',
            'raw': '2024-03-15 11:45:32 [Web Server] Unusual crawling behavior detected: IP 89.123.45.67 accessed /robots.txt, /admin, /wp-admin, /phpmyadmin, /.git in rapid succession. User-Agent: "Mozilla/5.0 (compatible; scanner/2.0)"',
            'source': 'Web Application Firewall',
            'severity': 'Low',
            'timestamp': '2024-03-15 11:45:32',
            'metadata': {
                'source_ip': '89.123.45.67',
                'paths_scanned': 23,
                'user_agent': 'Mozilla/5.0 (compatible; scanner/2.0)',
                'scan_duration': '3 minutes'
            },
            'explanation': 'Web scanning for common administrative interfaces and version control files indicates reconnaissance activity.',
            'phase': 'reconnaissance',
            'indicators': ['Directory scanning', 'Admin panel discovery', 'Automated tooling']
        }
    ],
    
    'weaponization': [
        {
            'id': 'weapon_1',
            'raw': '2024-03-16 14:12:45 [Email Security] Suspicious attachment detected: "Invoice_March2024.docm" contains obfuscated VBA macro with PowerShell download cradle. Hash matches known malware builder output.',
            'source': 'Email Security Gateway',
            'severity': 'High',
            'timestamp': '2024-03-16 14:12:45',
            'metadata': {
                'filename': 'Invoice_March2024.docm',
                'file_hash': 'a4b5c6d7e8f9g0h1i2j3',
                'macro_detected': True,
                'payload_type': 'PowerShell downloader'
            },
            'explanation': 'Malicious document with embedded macro represents weaponization phase where exploit is packaged with payload.',
            'phase': 'weaponization',
            'indicators': ['Macro-enabled document', 'Obfuscated code', 'Download cradle']
        },
        {
            'id': 'weapon_2',
            'raw': '2024-03-16 16:30:21 [Threat Intel] New malware sample uploaded to sandbox: PDF exploiting CVE-2024-1234 with embedded JavaScript that drops Cobalt Strike beacon. Document metadata shows creation 2 hours ago.',
            'source': 'Sandbox Analysis',
            'severity': 'High',
            'timestamp': '2024-03-16 16:30:21',
            'metadata': {
                'exploit': 'CVE-2024-1234',
                'payload': 'Cobalt Strike',
                'document_type': 'PDF',
                'creation_time': '2 hours ago'
            },
            'explanation': 'Fresh malware sample with recent exploit shows active weaponization of vulnerabilities.',
            'phase': 'weaponization',
            'indicators': ['Exploit packaging', 'Fresh malware', 'Known framework']
        }
    ],
    
    'delivery': [
        {
            'id': 'delivery_1',
            'raw': '2024-03-17 08:45:12 [Email Gateway] Phishing campaign detected: 47 emails sent to employees from "noreply@companysupport.tk" with subject "Urgent: Update Your Password". Contains link to credential harvesting site.',
            'source': 'Email Security',
            'severity': 'High',
            'timestamp': '2024-03-17 08:45:12',
            'metadata': {
                'sender': 'noreply@companysupport.tk',
                'recipients': 47,
                'subject': 'Urgent: Update Your Password',
                'malicious_url': 'hxxps://company-login[.]tk'
            },
            'explanation': 'Mass phishing email campaign represents delivery phase where weapon reaches targets.',
            'phase': 'delivery',
            'indicators': ['Phishing emails', 'Spoofed sender', 'Credential harvesting']
        },
        {
            'id': 'delivery_2',
            'raw': '2024-03-17 10:20:33 [Web Proxy] User clicked on malicious ad leading to exploit kit landing page. URL: hxxp://malicious-ads[.]com/campaign/loader.php redirected to Angler EK.',
            'source': 'Web Proxy',
            'severity': 'High',
            'timestamp': '2024-03-17 10:20:33',
            'metadata': {
                'initial_url': 'malicious-ads.com',
                'exploit_kit': 'Angler EK',
                'user': 'john.doe',
                'action': 'Blocked after detection'
            },
            'explanation': 'Malvertising leading to exploit kit shows delivery through compromised advertisements.',
            'phase': 'delivery',
            'indicators': ['Malicious redirect', 'Exploit kit', 'Drive-by download']
        }
    ],
    
    'exploitation': [
        {
            'id': 'exploit_1',
            'raw': '2024-03-18 11:15:43 [EDR] Process injection detected: winword.exe spawned powershell.exe with encoded command attempting to bypass AMSI. Memory analysis shows shellcode execution.',
            'source': 'Endpoint Detection',
            'severity': 'Critical',
            'timestamp': '2024-03-18 11:15:43',
            'metadata': {
                'parent_process': 'winword.exe',
                'child_process': 'powershell.exe',
                'technique': 'Process Injection',
                'amsi_bypass': True
            },
            'explanation': 'Malicious code execution from Word document indicates successful exploitation of vulnerability.',
            'phase': 'exploitation',
            'indicators': ['Process injection', 'AMSI bypass', 'Shellcode execution']
        },
        {
            'id': 'exploit_2',
            'raw': '2024-03-18 13:45:22 [SIEM] Exploitation attempt detected: Apache Log4j vulnerability (CVE-2021-44228) triggered via JNDI injection. Payload attempted to download secondary stage from 192.168.45.67.',
            'source': 'SIEM',
            'severity': 'Critical',
            'timestamp': '2024-03-18 13:45:22',
            'metadata': {
                'vulnerability': 'CVE-2021-44228',
                'attack_vector': 'JNDI injection',
                'payload_source': '192.168.45.67',
                'service': 'Apache Log4j'
            },
            'explanation': 'Log4Shell exploitation attempt shows active vulnerability exploitation phase.',
            'phase': 'exploitation',
            'indicators': ['Known CVE', 'Remote code execution', 'Payload download']
        }
    ],
    
    'installation': [
        {
            'id': 'install_1',
            'raw': '2024-03-19 15:23:11 [Sysmon] Registry persistence detected: New service "WindowsUpdateHelper" created pointing to C:\\ProgramData\\update.exe. File signed with invalid certificate, established scheduled task for hourly execution.',
            'source': 'Sysmon',
            'severity': 'High',
            'timestamp': '2024-03-19 15:23:11',
            'metadata': {
                'service_name': 'WindowsUpdateHelper',
                'file_path': 'C:\\ProgramData\\update.exe',
                'persistence_type': 'Service + Scheduled Task',
                'certificate': 'Invalid'
            },
            'explanation': 'Malware establishing persistence through services and scheduled tasks indicates installation phase.',
            'phase': 'installation',
            'indicators': ['Service creation', 'Scheduled task', 'Persistence mechanism']
        },
        {
            'id': 'install_2',
            'raw': '2024-03-19 16:45:33 [EDR] Rootkit installation detected: Hidden process "svchost.exe" running from %TEMP% directory with kernel-level hooks. SSDT modification observed.',
            'source': 'EDR System',
            'severity': 'Critical',
            'timestamp': '2024-03-19 16:45:33',
            'metadata': {
                'process': 'svchost.exe',
                'location': '%TEMP%',
                'technique': 'Rootkit',
                'kernel_modification': True
            },
            'explanation': 'Rootkit installation with kernel modifications shows advanced malware installation.',
            'phase': 'installation',
            'indicators': ['Rootkit behavior', 'Kernel hooks', 'Hidden process']
        }
    ],
    
    'command_control': [
        {
            'id': 'c2_1',
            'raw': '2024-03-20 09:12:45 [Network Monitor] Suspicious beaconing detected: Host 10.0.1.45 communicating with 185.234.219.11:443 every 60 seconds with jitter of 10%. Traffic pattern matches Cobalt Strike beacon.',
            'source': 'Network Security Monitor',
            'severity': 'Critical',
            'timestamp': '2024-03-20 09:12:45',
            'metadata': {
                'internal_host': '10.0.1.45',
                'c2_server': '185.234.219.11:443',
                'beacon_interval': '60 seconds',
                'protocol': 'HTTPS'
            },
            'explanation': 'Regular beaconing pattern to external server indicates established command and control channel.',
            'phase': 'command_control',
            'indicators': ['Beaconing behavior', 'Regular intervals', 'External communication']
        },
        {
            'id': 'c2_2',
            'raw': '2024-03-20 11:30:22 [DLP] Data exfiltration alert: Unusual DNS queries detected with base64 encoded data in subdomains to ns1.evil-domain.com. Total 450MB of data transmitted via DNS tunneling.',
            'source': 'Data Loss Prevention',
            'severity': 'Critical',
            'timestamp': '2024-03-20 11:30:22',
            'metadata': {
                'technique': 'DNS tunneling',
                'destination': 'ns1.evil-domain.com',
                'data_volume': '450MB',
                'encoding': 'Base64'
            },
            'explanation': 'DNS tunneling for data exfiltration shows active C2 channel being used for data theft.',
            'phase': 'command_control',
            'indicators': ['DNS tunneling', 'Data encoding', 'Large data transfer']
        }
    ],
    
    'actions_objectives': [
        {
            'id': 'action_1',
            'raw': '2024-03-21 14:45:33 [DLP] Mass data exfiltration detected: 15GB of sensitive files from Finance share compressed and uploaded to cloud storage. Files include "Q1_Financial_Report.xlsx", "Customer_Database.csv".',
            'source': 'Data Loss Prevention',
            'severity': 'Critical',
            'timestamp': '2024-03-21 14:45:33',
            'metadata': {
                'data_volume': '15GB',
                'file_types': ['Financial reports', 'Customer data'],
                'destination': 'Cloud storage',
                'compression': True
            },
            'explanation': 'Large-scale data theft indicates attacker achieving their objective of stealing sensitive information.',
            'phase': 'actions_objectives',
            'indicators': ['Data exfiltration', 'Sensitive files', 'Large volume']
        },
        {
            'id': 'action_2',
            'raw': '2024-03-21 16:20:11 [Security Alert] Ransomware deployment detected: All files on network shares being encrypted with .locked extension. Ransom note "PAY_TO_DECRYPT.txt" created in each directory.',
            'source': 'Endpoint Security',
            'severity': 'Critical',
            'timestamp': '2024-03-21 16:20:11',
            'metadata': {
                'ransomware_family': 'Unknown',
                'file_extension': '.locked',
                'ransom_note': 'PAY_TO_DECRYPT.txt',
                'affected_shares': 12
            },
            'explanation': 'Ransomware deployment represents final phase where attacker executes their primary objective.',
            'phase': 'actions_objectives',
            'indicators': ['File encryption', 'Ransom note', 'Mass impact']
        }
    ]
}

# ============================================================================
# STRATEGIE DI MITIGAZIONE PER FASE
# ============================================================================

MITIGATION_STRATEGIES = {
    'reconnaissance': [
        {
            'id': 'recon_mit_1',
            'name': 'Reduce Attack Surface',
            'description': 'Limit publicly exposed services and information',
            'icon': '🛡️',
            'effectiveness': 'High'
        },
        {
            'id': 'recon_mit_2',
            'name': 'Threat Intelligence Monitoring',
            'description': 'Monitor for reconnaissance activities targeting your organization',
            'icon': '📊',
            'effectiveness': 'Medium'
        },
        {
            'id': 'recon_mit_3',
            'name': 'Honeypots and Deception',
            'description': 'Deploy decoy systems to detect and mislead attackers',
            'icon': '🍯',
            'effectiveness': 'Medium'
        },
        {
            'id': 'recon_mit_4',
            'name': 'DNS Monitoring',
            'description': 'Monitor and alert on suspicious DNS queries',
            'icon': '🔍',
            'effectiveness': 'High'
        }
    ],
    
    'weaponization': [
        {
            'id': 'weapon_mit_1',
            'name': 'Threat Intelligence Feeds',
            'description': 'Subscribe to IOC feeds to detect known malware',
            'icon': '📰',
            'effectiveness': 'High'
        },
        {
            'id': 'weapon_mit_2',
            'name': 'Vulnerability Management',
            'description': 'Patch systems to prevent exploit weaponization',
            'icon': '🔧',
            'effectiveness': 'High'
        },
        {
            'id': 'weapon_mit_3',
            'name': 'Security Awareness Training',
            'description': 'Train users to recognize weaponized content',
            'icon': '🎓',
            'effectiveness': 'Medium'
        },
        {
            'id': 'weapon_mit_4',
            'name': 'Sandbox Analysis',
            'description': 'Analyze suspicious files in isolated environment',
            'icon': '📦',
            'effectiveness': 'High'
        }
    ],
    
    'delivery': [
        {
            'id': 'delivery_mit_1',
            'name': 'Email Security Gateway',
            'description': 'Filter malicious emails and attachments',
            'icon': '📧',
            'effectiveness': 'High'
        },
        {
            'id': 'delivery_mit_2',
            'name': 'Web Filtering',
            'description': 'Block access to malicious websites',
            'icon': '🌐',
            'effectiveness': 'High'
        },
        {
            'id': 'delivery_mit_3',
            'name': 'Disable Macros',
            'description': 'Block macro execution in office documents',
            'icon': '📄',
            'effectiveness': 'High'
        },
        {
            'id': 'delivery_mit_4',
            'name': 'Application Whitelisting',
            'description': 'Only allow approved applications to run',
            'icon': '✅',
            'effectiveness': 'Very High'
        }
    ],
    
    'exploitation': [
        {
            'id': 'exploit_mit_1',
            'name': 'Patch Management',
            'description': 'Apply security patches immediately',
            'icon': '🔄',
            'effectiveness': 'Very High'
        },
        {
            'id': 'exploit_mit_2',
            'name': 'EDR Solution',
            'description': 'Deploy endpoint detection and response',
            'icon': '💻',
            'effectiveness': 'High'
        },
        {
            'id': 'exploit_mit_3',
            'name': 'Network Segmentation',
            'description': 'Isolate critical systems from general network',
            'icon': '🔗',
            'effectiveness': 'High'
        },
        {
            'id': 'exploit_mit_4',
            'name': 'Exploit Protection',
            'description': 'Enable DEP, ASLR, and CFG protections',
            'icon': '🛡️',
            'effectiveness': 'Medium'
        }
    ],
    
    'installation': [
        {
            'id': 'install_mit_1',
            'name': 'Application Control',
            'description': 'Prevent unauthorized software installation',
            'icon': '🚫',
            'effectiveness': 'Very High'
        },
        {
            'id': 'install_mit_2',
            'name': 'Privilege Management',
            'description': 'Remove local admin rights from users',
            'icon': '👤',
            'effectiveness': 'High'
        },
        {
            'id': 'install_mit_3',
            'name': 'Registry Monitoring',
            'description': 'Alert on suspicious registry modifications',
            'icon': '📝',
            'effectiveness': 'Medium'
        },
        {
            'id': 'install_mit_4',
            'name': 'File Integrity Monitoring',
            'description': 'Detect unauthorized system file changes',
            'icon': '📁',
            'effectiveness': 'High'
        }
    ],
    
    'command_control': [
        {
            'id': 'c2_mit_1',
            'name': 'Network Traffic Analysis',
            'description': 'Detect anomalous outbound connections',
            'icon': '📡',
            'effectiveness': 'High'
        },
        {
            'id': 'c2_mit_2',
            'name': 'DNS Sinkholing',
            'description': 'Redirect malicious domains to internal server',
            'icon': '🕳️',
            'effectiveness': 'High'
        },
        {
            'id': 'c2_mit_3',
            'name': 'Firewall Rules',
            'description': 'Block unauthorized outbound connections',
            'icon': '🔥',
            'effectiveness': 'High'
        },
        {
            'id': 'c2_mit_4',
            'name': 'SSL/TLS Inspection',
            'description': 'Decrypt and inspect encrypted traffic',
            'icon': '🔐',
            'effectiveness': 'Medium'
        }
    ],
    
    'actions_objectives': [
        {
            'id': 'action_mit_1',
            'name': 'Data Backup and Recovery',
            'description': 'Maintain offline backups for ransomware recovery',
            'icon': '💾',
            'effectiveness': 'Very High'
        },
        {
            'id': 'action_mit_2',
            'name': 'DLP Solutions',
            'description': 'Prevent unauthorized data exfiltration',
            'icon': '🔒',
            'effectiveness': 'High'
        },
        {
            'id': 'action_mit_3',
            'name': 'Incident Response Plan',
            'description': 'Execute prepared response procedures',
            'icon': '🚨',
            'effectiveness': 'High'
        },
        {
            'id': 'action_mit_4',
            'name': 'Network Isolation',
            'description': 'Immediately isolate affected systems',
            'icon': '🔌',
            'effectiveness': 'High'
        }
    ]
}

# ============================================================================
# GESTIONE SESSIONI
# ============================================================================

user_sessions = {}

# ============================================================================
# FUNZIONI HELPER
# ============================================================================

def calculate_difficulty(score, streak, accuracy):
    """Calcola difficoltà basata sulle performance"""
    performance_score = (score * 0.3) + (streak * 10) + (accuracy * 0.4)
    
    if performance_score < 50:
        return 'beginner'
    elif performance_score < 150:
        return 'intermediate'
    else:
        return 'expert'

def get_random_log(difficulty='all'):
    """Ottiene un log casuale dal database"""
    # Per difficoltà beginner, usa solo le prime 3 fasi
    # Per intermediate, usa le prime 5 fasi
    # Per expert, usa tutte le 7 fasi
    
    if difficulty == 'beginner':
        phases = ['reconnaissance', 'weaponization', 'delivery']
    elif difficulty == 'intermediate':
        phases = ['reconnaissance', 'weaponization', 'delivery', 'exploitation', 'installation']
    else:  # expert or all
        phases = list(LOGS_DATABASE.keys())
    
    selected_phase = random.choice(phases)
    selected_log = random.choice(LOGS_DATABASE[selected_phase])
    
    return selected_log, selected_phase

def calculate_points(difficulty, time_remaining, phase_correct, mitigation_correct):
    """Calcola i punti guadagnati"""
    base_points = {
        'beginner': 10,
        'intermediate': 25,
        'expert': 50
    }
    
    points = 0
    
    # Punti per fase corretta
    if phase_correct:
        points += base_points.get(difficulty, 10)
        
        # Punti per mitigazione corretta (solo se fase è corretta)
        if mitigation_correct:
            points += base_points.get(difficulty, 10)
            
            # Bonus tempo
            time_bonus = int(time_remaining * 0.5)
            points += time_bonus
    
    return points

# ============================================================================
# ENDPOINTS API
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'game': 'Cyber Kill Chain Analyzer'
    })

@app.route('/api/get-phases', methods=['GET'])
def get_phases():
    """Ottiene tutte le fasi della Cyber Kill Chain"""
    phases = []
    for key, value in CYBER_KILL_CHAIN_PHASES.items():
        phases.append({
            'id': key,
            'name': value['name'],
            'description': value['description'],
            'icon': value['icon']
        })
    return jsonify({'phases': phases})

@app.route('/api/get-log', methods=['POST'])
def get_log():
    """Ottiene un nuovo log da analizzare"""
    data = request.json
    session_id = data.get('session_id', 'default')
    difficulty = data.get('difficulty', 'beginner')
    
    # Seleziona un log casuale basato sulla difficoltà
    selected_log, selected_phase = get_random_log(difficulty)
    
    # Salva la risposta corretta in sessione
    if session_id not in user_sessions:
        user_sessions[session_id] = {}
    
    user_sessions[session_id]['current_log'] = selected_log['id']
    user_sessions[session_id]['correct_phase'] = selected_phase
    user_sessions[session_id]['log_data'] = selected_log
    
    # Prepara il log per il client (senza la soluzione)
    response_log = {
        'id': selected_log['id'],
        'raw': selected_log['raw'],
        'source': selected_log['source'],
        'severity': selected_log['severity'],
        'timestamp': selected_log['timestamp'],
        'metadata': selected_log['metadata']
    }
    
    # Tempo limite basato sulla difficoltà
    time_limits = {
        'beginner': 90,
        'intermediate': 60,
        'expert': 45
    }
    
    return jsonify({
        'log': response_log,
        'time_limit': time_limits.get(difficulty, 60)
    })

@app.route('/api/validate-phase', methods=['POST'])
def validate_phase():
    """Valida la fase selezionata dall'utente"""
    data = request.json
    session_id = data.get('session_id', 'default')
    selected_phase = data.get('selected_phase')
    
    session = user_sessions.get(session_id, {})
    correct_phase = session.get('correct_phase')
    log_data = session.get('log_data', {})
    
    is_correct = selected_phase == correct_phase
    
    if is_correct:
        # Se corretto, prepara le strategie di mitigazione
        mitigation_options = MITIGATION_STRATEGIES.get(correct_phase, [])
        
        # Salva la mitigazione corretta in sessione (seleziona quella più efficace)
        correct_mitigation = random.choice([m for m in mitigation_options if m['effectiveness'] in ['High', 'Very High']])
        user_sessions[session_id]['correct_mitigation'] = correct_mitigation['id']
        
        return jsonify({
            'is_correct': True,
            'mitigation_strategies': mitigation_options,
            'explanation': log_data.get('explanation', ''),
            'indicators': log_data.get('indicators', [])
        })
    else:
        return jsonify({
            'is_correct': False,
            'correct_phase': correct_phase,
            'phase_info': CYBER_KILL_CHAIN_PHASES[correct_phase],
            'explanation': log_data.get('explanation', ''),
            'indicators': log_data.get('indicators', [])
        })

@app.route('/api/validate-mitigation', methods=['POST'])
def validate_mitigation():
    """Valida la strategia di mitigazione selezionata"""
    data = request.json
    session_id = data.get('session_id', 'default')
    selected_mitigation = data.get('selected_mitigation')
    time_remaining = data.get('time_remaining', 0)
    difficulty = data.get('difficulty', 'beginner')
    
    session = user_sessions.get(session_id, {})
    correct_mitigation = session.get('correct_mitigation')
    correct_phase = session.get('correct_phase')
    
    # Verifica se la mitigazione è appropriata
    phase_mitigations = MITIGATION_STRATEGIES.get(correct_phase, [])
    selected_mit_data = next((m for m in phase_mitigations if m['id'] == selected_mitigation), None)
    
    # Considera corretta se l'efficacia è High o Very High
    is_correct = selected_mit_data and selected_mit_data['effectiveness'] in ['High', 'Very High']
    
    # Calcola punti
    points = calculate_points(difficulty, time_remaining, True, is_correct)
    
    return jsonify({
        'is_correct': is_correct,
        'points': points,
        'selected_effectiveness': selected_mit_data['effectiveness'] if selected_mit_data else 'None',
        'best_mitigation': next((m for m in phase_mitigations if m['id'] == correct_mitigation), None)
    })

@app.route('/api/statistics', methods=['POST'])
def get_statistics():
    """Ottiene statistiche dell'utente"""
    data = request.json
    session_id = data.get('session_id', 'default')
    
    # In produzione, queste verrebbero dal database
    stats = {
        'total_games': 0,
        'phases_mastered': [],
        'average_accuracy': 0,
        'favorite_phase': 'reconnaissance',
        'achievements': []
    }
    
    return jsonify(stats)

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Ottiene la classifica globale"""
    # Mock data per dimostrazione
    leaderboard = [
        {'rank': 1, 'name': 'CyberHunter', 'score': 2150, 'mastery': '7/7 phases'},
        {'rank': 2, 'name': 'SecurityPro', 'score': 1890, 'mastery': '6/7 phases'},
        {'rank': 3, 'name': 'KillChainMaster', 'score': 1750, 'mastery': '7/7 phases'},
        {'rank': 4, 'name': 'ThreatAnalyst', 'score': 1620, 'mastery': '5/7 phases'},
        {'rank': 5, 'name': 'BlueTeamer', 'score': 1500, 'mastery': '4/7 phases'}
    ]
    
    return jsonify({'leaderboard': leaderboard})

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, port=5000)