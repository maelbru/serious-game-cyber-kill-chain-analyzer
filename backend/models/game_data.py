"""
CYBER KILL CHAIN ANALYZER - MODELLI E DATI DEL GIOCO

Questo file contiene tutti i dati statici utilizzati dall'applicazione:
- Definizioni delle fasi della Cyber Kill Chain
- Database dei log di sicurezza per ogni fase
- Strategie di mitigazione per ciascuna fase
- Configurazioni per i livelli di difficoltà

È essenzialmente il "database" in-memory dell'applicazione educativa.
"""

from datetime import datetime

# ============================================================================
# DEFINIZIONE DELLE FASI DELLA CYBER KILL CHAIN
# Basato sul framework di Lockheed Martin per la cybersecurity
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
# DATABASE DEI LOG DI SICUREZZA
# Organizzato per fase della kill chain con log realistici per l'educazione
# ============================================================================

LOGS_DATABASE = {
    # --- FASE 1: RECONNAISSANCE ---
    # Log che mostrano attività di ricognizione e raccolta informazioni
    'reconnaissance': [
        {
            'id': 'recon_1',
            # Log raw come apparirebbe in un SIEM reale
            'raw': '2025-03-15 09:23:17 [IDS] Multiple DNS queries detected from external IP 185.234.218.12 for domain controllers, mail servers, and VPN endpoints. Pattern suggests automated reconnaissance tool usage.',
            'source': 'Network IDS',              # Sistema che ha generato il log
            'severity': 'Low',                    # Livello di gravità dell'evento
            'timestamp': '2025-03-15 09:23:17',  # Quando è avvenuto l'evento
            'metadata': {                        # Dati strutturati per analisi
                'source_ip': '185.234.218.12',
                'queries': 47,
                'targets': ['dc01.company.local', 'mail.company.local', 'vpn.company.local'],
                'tool_signature': 'nmap/dnsrecon'
            },
            # Spiegazione educativa (nascosta al giocatore inizialmente)
            'explanation': 'Query DNS multiple verso componenti dell\'infrastruttura indicano la fase di ricognizione, in cui gli attaccanti mappano la rete.',
            'phase': 'reconnaissance',
            # Indicatori chiave che dovrebbero far identificare la fase
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
                'target_ports': [22, 23, 80, 443, 3389, 5985],  # Porte comuni per servizi
                'scan_type': 'TCP SYN Scan',
                'duration': '15 minutes'
            },
            'explanation': 'Scansione sistematica delle porte comuni indica attività di reconnaissance per identificare servizi esposti.',
            'phase': 'reconnaissance',
            'indicators': ['Port scanning', 'Enumerazione servizi', 'Mappatura superficie d\'attacco']
        }
    ],
    
    # --- FASE 2: WEAPONIZATION ---
    # Log che mostrano la creazione di armi digitali (malware, exploit)
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
    
    # --- FASE 3: DELIVERY ---
    # Log che mostrano la consegna del malware al target
    'delivery': [
        {
            'id': 'delivery_1',
            'raw': '2025-03-17 08:45:12 [Email Gateway] Phishing campaign detected: 47 emails sent to employees from "noreply@companysupport.tk" with subject "Urgent: Update Your Password". Contains link to credential harvesting site.',
            'source': 'Email Security',
            'severity': 'High',
            'timestamp': '2025-03-17 08:45:12',
            'metadata': {
                'sender': 'noreply@companysupport.tk',  # Dominio sospetto
                'recipients': 47,
                'subject': 'Urgent: Update Your Password',
                'malicious_url': 'hxxps://company-login[.]tk'  # URL defanged per sicurezza
            },
            'explanation': 'Una campagna di phishing di massa rappresenta la fase di delivery, in cui il payload raggiunge i bersagli.',
            'phase': 'delivery',
            'indicators': ['Email di phishing', 'Mittente contraffatto', 'Raccolta di credenziali']
        }
    ],
    
    # --- FASE 4: EXPLOITATION ---
    # Log che mostrano lo sfruttamento di vulnerabilità
    'exploitation': [
        {
            'id': 'exploit_1',
            'raw': '2025-03-18 11:15:43 [EDR] Process injection detected: winword.exe spawned powershell.exe with encoded command attempting to bypass AMSI. Memory analysis shows shellcode execution.',
            'source': 'Endpoint Detection',
            'severity': 'Critical',
            'timestamp': '2025-03-18 11:15:43',
            'metadata': {
                'parent_process': 'winword.exe',      # Processo padre legittimo
                'child_process': 'powershell.exe',    # Processo figlio sospetto
                'technique': 'Process Injection',
                'amsi_bypass': True                   # Tentativo di evasione
            },
            'explanation': 'L\'esecuzione di codice malevolo da un documento Word indica l\'avvenuta exploitation di una vulnerabilità.',
            'phase': 'exploitation',
            'indicators': ['Iniezione di processo', 'Bypass di AMSI', 'Esecuzione di shellcode']
        }
    ],
    
    # --- FASE 5: INSTALLATION ---
    # Log che mostrano l'installazione persistente di malware
    'installation': [
        {
            'id': 'install_1',
            'raw': '2025-03-19 15:23:11 [Sysmon] Registry persistence detected: New service "WindowsUpdateHelper" created pointing to C:\\ProgramData\\update.exe. File signed with invalid certificate, established scheduled task for hourly execution.',
            'source': 'Sysmon',
            'severity': 'High',
            'timestamp': '2025-03-19 15:23:11',
            'metadata': {
                'service_name': 'WindowsUpdateHelper',    # Nome ingannevole
                'file_path': 'C:\\ProgramData\\update.exe',
                'persistence_type': 'Service + Scheduled Task',  # Doppia persistenza
                'certificate': 'Invalid'
            },
            'explanation': 'Il malware che stabilisce persistenza tramite servizi e attività pianificate indica la fase di installation',
            'phase': 'installation',
            'indicators': ['Creazione di servizio', 'Attività pianificata', 'Meccanismo di persistenza']
        }
    ],
    
    # --- FASE 6: COMMAND & CONTROL ---
    # Log che mostrano comunicazioni C2
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
                'beacon_interval': '60 seconds',   # Intervallo regolare tipico di C2
                'protocol': 'HTTPS'                # Usa protocollo legittimo per mimetizzarsi
            },
            'explanation': 'Un pattern regolare di beaconing verso un server esterno indica l\'avvenuta creazione di un canale di command and control.',
            'phase': 'command_control',
            'indicators': ['Comportamento di beaconing', 'Intervalli regolari', 'Comunicazione esterna']
        }
    ],
    
    # --- FASE 7: ACTIONS ON OBJECTIVES ---
    # Log che mostrano il raggiungimento degli obiettivi finali
    'actions_objectives': [
        {
            'id': 'action_1',
            'raw': '2025-03-21 14:45:33 [DLP] Mass data exfiltration detected: 15GB of sensitive files from Finance share compressed and uploaded to cloud storage. Files include "Q1_Financial_Report.xlsx", "Customer_Database.csv".',
            'source': 'Data Loss Prevention',
            'severity': 'Critical',
            'timestamp': '2025-03-21 14:45:33',
            'metadata': {
                'data_volume': '15GB',                    # Grande volume indica esfiltrazione
                'file_types': ['Financial reports', 'Customer data'],
                'destination': 'Cloud storage',
                'compression': True                       # Compressi per eludere DLP
            },
            'explanation': 'Il furto su larga scala di dati indica che l\'attaccante ha raggiunto l\'obiettivo di sottrarre informazioni sensibili.',
            'phase': 'actions_objectives',
            'indicators': ['Esfiltrazione di dati', 'File sensibili', 'Grande volume di dati']
        }
    ]
}

# ============================================================================
# STRATEGIE DI MITIGAZIONE PER OGNI FASE
# Contromisure reali utilizzate nell'industry per ogni fase della kill chain
# ============================================================================

MITIGATION_STRATEGIES = {
    # Mitigazioni per la fase di reconnaissance
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
    
    # Mitigazioni per la fase di weaponization
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
    
    # Mitigazioni per la fase di delivery
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
            'effectiveness': 'Very High'  # Efficacia massima
        }
    ],
    
    # Mitigazioni per la fase di exploitation
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
    
    # Mitigazioni per la fase di installation
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
    
    # Mitigazioni per la fase di command & control
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
    
    # Mitigazioni per la fase di actions on objectives
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
# CONFIGURAZIONE DEI LIVELLI DI DIFFICOLTÀ
# Definisce parametri e limitazioni per ogni livello di gioco
# ============================================================================

DIFFICULTY_CONFIG = {
    'beginner': {
        'phases': ['reconnaissance', 'weaponization', 'delivery'],  # Solo 3 fasi più semplici
        'time_limit': 60,          # 60 secondi per rispondere
        'base_points': 10          # Punti base per risposta corretta
    },
    'intermediate': {
        'phases': ['reconnaissance', 'weaponization', 'delivery', 'exploitation', 'installation'],  # 5 fasi
        'time_limit': 40,          # 40 secondi per rispondere  
        'base_points': 25          # Più punti per maggiore difficoltà
    },
    'expert': {
        'phases': list(LOGS_DATABASE.keys()),  # Tutte e 7 le fasi
        'time_limit': 30,          # Solo 30 secondi per rispondere
        'base_points': 50          # Massimo punteggio per esperti
    }
}