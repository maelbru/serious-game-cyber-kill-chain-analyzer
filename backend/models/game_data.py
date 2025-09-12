"""
CYBER KILL CHAIN ANALYZER - GAME DATA MODELS
Tutti i dati statici, configurazione e database in-memory
"""

from datetime import datetime

# ============================================================================
# CYBER KILL CHAIN PHASES CONFIGURATION
# ============================================================================

CYBER_KILL_CHAIN_PHASES = {
    'reconnaissance': {
        'name': 'Reconnaissance',
        'description': 'L\'attaccante raccoglie informazioni sul bersaglio',
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
        'description': 'Raggiungimento degli obiettivi dell\'attaccante',
        'icon': '🎯'
    }
}

# ============================================================================
# SECURITY LOGS DATABASE
# ============================================================================

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
            'explanation': 'Query DNS multiple verso componenti dell\'infrastruttura indicano la fase di ricognizione, in cui gli attaccanti mappano la rete.',
            'phase': 'reconnaissance',
            'indicators': ['Enumerazione DNS', 'Scansione esterna', 'Mappatura dell\'infrastruttura']
        },
        {
            'id': 'recon_2',
            'raw': '2025-03-15 14:12:33 [Firewall] Port scan detected from 203.0.113.42 targeting TCP ports 22, 23, 80, 443, 3389, 5985. Scan pattern indicates systematic enumeration.',
            'source': 'Firewall Logs',
            'severity': 'Medium',
            'timestamp': '2025-03-15 14:12:33',
            'metadata': {
                'source_ip': '203.0.113.42',
                'target_ports': [22, 23, 80, 443, 3389, 5985],
                'scan_type': 'TCP SYN Scan',
                'duration': '15 minutes'
            },
            'explanation': 'Scansione sistematica delle porte comuni indica attività di reconnaissance per identificare servizi esposti.',
            'phase': 'reconnaissance',
            'indicators': ['Port scanning', 'Enumerazione servizi', 'Mappatura superficie d\'attacco']
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
            'explanation': 'Documento malevolo con macro incorporata rappresenta la fase di weaponization, in cui l\'exploit viene confezionato insieme al payload.',
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
            'explanation': 'L\'esecuzione di codice malevolo da un documento Word indica l\'avvenuta exploitation di una vulnerabilità.',
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
            'explanation': 'Un pattern regolare di beaconing verso un server esterno indica l\'avvenuta creazione di un canale di command and control.',
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
            'explanation': 'Il furto su larga scala di dati indica che l\'attaccante ha raggiunto l\'obiettivo di sottrarre informazioni sensibili.',
            'phase': 'actions_objectives',
            'indicators': ['Esfiltrazione di dati', 'File sensibili', 'Grande volume di dati']
        }
    ]
}

# ============================================================================
# MITIGATION STRATEGIES DATABASE
# ============================================================================

MITIGATION_STRATEGIES = {
    'reconnaissance': [
        {
            'id': 'recon_mit_1',
            'name': 'Riduzione della superficie d\'attacco',
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
            'description': 'Consentire l\'esecuzione solo ad applicazioni approvate',
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
            'name': 'Soluzione EDR',
            'description': 'Implementare soluzioni di rilevamento e risposta sugli endpoint',
            'icon': '💻',
            'effectiveness': 'High'
        }
    ],
    'installation': [
        {
            'id': 'install_mit_1',
            'name': 'Controllo delle applicazioni',
            'description': 'Impedire l\'installazione di software non autorizzato',
            'icon': '🚫',
            'effectiveness': 'Very High'
        },
        {
            'id': 'install_mit_2',
            'name': 'Monitoraggio dell\'integrità dei file',
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
            'name': 'Soluzioni DLP',
            'description': 'Impedire l\'esfiltrazione non autorizzata di dati',
            'icon': '🔒',
            'effectiveness': 'High'
        }
    ]
}

# ============================================================================
# DIFFICULTY CONFIGURATION
# ============================================================================

DIFFICULTY_CONFIG = {
    'beginner': {
        'phases': ['reconnaissance', 'weaponization', 'delivery'],
        'time_limit': 60,
        'base_points': 10
    },
    'intermediate': {
        'phases': ['reconnaissance', 'weaponization', 'delivery', 'exploitation', 'installation'],
        'time_limit': 40,
        'base_points': 25
    },
    'expert': {
        'phases': list(LOGS_DATABASE.keys()),
        'time_limit': 30,
        'base_points': 50
    }
}