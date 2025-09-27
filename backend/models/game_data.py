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
        'name': 'Ricognizione',
        'description': 'L\'attaccante raccoglie informazioni sul bersaglio',
        'icon': '🔍'
    },
    'weaponization': {
        'name': 'Armamento', 
        'description': 'Creazione di un carico dannoso unito a un exploit',
        'icon': '🔨'
    },
    'delivery': {
        'name': 'Consegna',
        'description': 'Trasmissione del carico dannoso al bersaglio',
        'icon': '📧'
    },
    'exploitation': {
        'name': 'Sfruttamento',
        'description': 'Attivazione del codice exploit sul sistema vittima',
        'icon': '💥'
    },
    'installation': {
        'name': 'Installazione',
        'description': 'Installazione di malware sul sistema bersaglio',
        'icon': '⚙️'
    },
    'command_control': {
        'name': 'Comando e Controllo',
        'description': 'Creazione di un canale per il controllo remoto',
        'icon': '📡'
    },
    'actions_objectives': {
        'name': 'Azioni sugli Obiettivi',
        'description': 'Raggiungimento degli obiettivi dell\'attaccante',
        'icon': '🎯'
    }
}

# ============================================================================
# DATABASE DEI LOG DI SICUREZZA
# Organizzato per fase della kill chain con log realistici per l'educazione
# ============================================================================

LOGS_AND_SE_DATABASE = {
    # --- FASE 1: RECONNAISSANCE ---
    # Log che mostrano attività di ricognizione e raccolta informazioni
    'reconnaissance': [
        {
            'id': 'recon_1',
            # Log raw come apparirebbe in un SIEM reale
            'raw': '2025-03-15 09:23:17 [IDS] Multiple DNS queries detected from external IP 185.234.218.12 for domain controllers, mail servers, and VPN endpoints. Pattern suggests automated reconnaissance tool usage.',
            'source': 'IDS di Rete',                                # Sistema che ha generato il log
            'severity': 'Bassa',                                    # Livello di gravità dell'evento
            'timestamp': '2025-03-15 09:23:17',                     # Quando è avvenuto l'evento
            'metadata': {                                           # Dati strutturati per analisi
                'source_ip': '185.234.218.12',
                'queries': 47,
                'targets': ['dc01.company.local'],
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
            'source': 'Log Firewall',
            'severity': 'Media',
            'timestamp': '2025-03-15 14:12:33',
            'metadata': {
                'source_ip': '203.0.113.42',
                'target_ports': [22, 23, 80, 443, 3389, 5985],  # Porte comuni per servizi
                'scan_type': 'TCP SYN Scan',
                'duration': '15 minutes'
            },
            'explanation': 'Scansione sistematica delle porte comuni indica attività di ricognizione per identificare servizi esposti.',
            'phase': 'reconnaissance',
            'indicators': ['Scansione porte', 'Enumerazione servizi', 'Mappatura superficie d\'attacco']
        },
        {
            'id': 'social_recon_1',
            'raw': '2025-03-15 14:32:45 [PHONE_LOG] Chiamata da numero sconosciuto +39-06-45782341 diretta alla reception aziendale. Caller si è spacciato per tecnico IT richiedendo informazioni sui responsabili di sistema e l\'architettura di rete. Durata chiamata: 8 minuti.',
            'source': 'Sistema Telefonico Aziendale',
            'severity': 'Media',
            'timestamp': '2025-03-15 14:32:45',
            'metadata': {
                'caller_number': '+39-06-45782341',
                'target_department': 'reception',
                'duration_minutes': 8,
                'requested_info': ['responsabili_sistema', 'architettura_rete']
            },
            'explanation': 'Tentativo di social engineering telefonico per raccogliere informazioni sensibili sull\'organizzazione IT aziendale durante la fase di ricognizione.',
            'phase': 'reconnaissance',
            'indicators': ['Chiamata da numero sconosciuto', 'Richiesta informazioni IT', 'Impersonificazione tecnico']
        }
    ],
    
    # --- FASE 2: WEAPONIZATION ---
    # Log che mostrano la creazione di armi digitali (malware, exploit)
    'weaponization': [
        {
            'id': 'weapon_1',
            'raw': '2025-03-16 14:12:45 [Email Security] Suspicious attachment detected: "Invoice_March2025.docm" contains obfuscated VBA macro with PowerShell download cradle. Hash matches known malware builder output.',
            'source': 'Gateway di Sicurezza Email',
            'severity': 'Alta',
            'timestamp': '2025-03-16 14:12:45',
            'metadata': {
                'filename': 'Invoice_March2025.docm',
                'file_hash': 'a4b5c6d7e8f9g0h1i2j3',
                'macro_detected': True,
                'payload_type': 'PowerShell downloader'
            },
            'explanation': 'Documento dannoso con macro incorporata rappresenta la fase di armamento, in cui l\'exploit viene confezionato insieme al carico dannoso.',
            'phase': 'weaponization',
            'indicators': ['Documento con macro abilitate', 'Codice offuscato', 'Script di download']
        },
        {
            'id': 'social_weapon_1',
            'raw': '2025-03-15 16:18:22 [EMAIL_SECURITY] Email intercettata da mario.rossi@company.local con mittente falsificato hr@company.local. Oggetto: "Aggiornamento Urgente Policy Sicurezza". Allegato: PolicyUpdate_Q1_2025.exe (2.3MB). Email crafted per sembrare comunicazione HR ufficiale.',
            'source': 'Gateway Email Security',
            'severity': 'Alta',
            'timestamp': '2025-03-15 16:18:22',
            'metadata': {
                'sender_spoofed': 'hr@company.local',
                'recipient': 'mario.rossi@company.local',
                'attachment': 'PolicyUpdate_Q1_2025.exe',
                'file_size': '2.3MB',
                'social_trigger': 'urgenza_policy'
            },
            'explanation': 'Weaponization attraverso social engineering: creazione di email con allegato malevolo mascherato da comunicazione HR urgente per sfruttare l\'autorità e l\'urgenza.',
            'phase': 'weaponization',
            'indicators': ['Mittente falsificato HR', 'Comunicazione urgente', 'Allegato eseguibile mascherato']
        }
    ],
    
    # --- FASE 3: DELIVERY ---
    # Log che mostrano la consegna del malware al target
    'delivery': [
        {
            'id': 'delivery_1',
            'raw': '2025-03-17 08:45:12 [Email Gateway] Phishing campaign detected: 47 emails sent to employees from "noreply@companysupport.tk" with subject "Urgent: Update Your Password". Contains link to credential harvesting site.',
            'source': 'Sicurezza Email',
            'severity': 'Alta',
            'timestamp': '2025-03-17 08:45:12',
            'metadata': {
                'sender': 'noreply@companysupport.tk',  # Dominio sospetto
                'recipients': 47,
                'subject': 'Urgente: Aggiorna la Tua Password',
                'malicious_url': 'hxxps://company-login[.]tk'  # URL defanged per sicurezza
            },
            'explanation': 'Una campagna di phishing di massa rappresenta la fase di consegna, in cui il carico dannoso raggiunge i bersagli.',
            'phase': 'delivery',
            'indicators': ['Email di phishing', 'Mittente contraffatto', 'Raccolta di credenziali']
        },
        {
            'id': 'social_delivery_1',
            'raw': '2025-03-15 11:47:33 [EMAIL_GATEWAY] Email phishing consegnata a 15 dipendenti del reparto contabilità. Mittente: ceo@comp4ny.com (typosquatting). Oggetto: "URGENTE: Bonifico immediato per acquisizione". Testo richiede trasferimento fondi con bypass delle procedure standard.',
            'source': 'Email Gateway',
            'severity': 'Critica',
            'timestamp': '2025-03-15 11:47:33',
            'metadata': {
                'recipients_count': 15,
                'target_department': 'contabilità',
                'sender_domain': 'comp4ny.com',
                'attack_type': 'CEO_fraud',
                'requested_action': 'trasferimento_fondi'
            },
            'explanation': 'Consegna di attacco BEC (Business Email Compromise) mirato al reparto contabilità, utilizzando impersonificazione del CEO per ottenere trasferimenti di denaro.',
            'phase': 'delivery',
            'indicators': ['Typosquatting del dominio', 'Impersonificazione CEO', 'Richiesta bypass procedure']
        }
    ],
    
    # --- FASE 4: EXPLOITATION ---
    # Log che mostrano lo sfruttamento di vulnerabilità
    'exploitation': [
        {
            'id': 'exploit_1',
            'raw': '2025-03-18 11:15:43 [EDR] Process injection detected: winword.exe spawned powershell.exe with encoded command attempting to bypass AMSI. Memory analysis shows shellcode execution.',
            'source': 'Rilevamento Endpoint',
            'severity': 'Critica',
            'timestamp': '2025-03-18 11:15:43',
            'metadata': {
                'parent_process': 'winword.exe',      # Processo padre legittimo
                'child_process': 'powershell.exe',    # Processo figlio sospetto
                'technique': 'Process Injection',
                'amsi_bypass': True                   # Tentativo di evasione
            },
            'explanation': 'L\'esecuzione di codice dannoso da un documento Word indica l\'avvenuto sfruttamento di una vulnerabilità.',
            'phase': 'exploitation',
            'indicators': ['Iniezione di processo', 'Bypass di AMSI', 'Esecuzione di shellcode']
        },
        {
            'id': 'social_exploit_1',
            'raw': '2025-03-15 13:25:17 [USER_BEHAVIOR] Utente laura.bianchi@company.local ha inserito credenziali su sito falso login-company-portal.com dopo aver ricevuto SMS di reset password. Sessione browser redirect da link abbreviato bit.ly/comp-reset. Credenziali compromesse.',
            'source': 'Behavioral Analytics',
            'severity': 'Alta',
            'timestamp': '2025-03-15 13:25:17',
            'metadata': {
                'compromised_user': 'laura.bianchi@company.local',
                'fake_site': 'login-company-portal.com',
                'delivery_method': 'SMS',
                'redirect_source': 'bit.ly/comp-reset',
                'credentials_harvested': True
            },
            'explanation': 'Sfruttamento di tecniche di social engineering via SMS phishing per ottenere credenziali dell\'utente attraverso sito clone del portale aziendale.',
            'phase': 'exploitation',
            'indicators': ['Sito clone aziendale', 'SMS phishing', 'Credential harvesting']
        }
    ],
    
    # --- FASE 5: INSTALLATION ---
    # Log che mostrano l'installazione persistente di malware
    'installation': [
        {
            'id': 'install_1',
            'raw': '2025-03-19 15:23:11 [Sysmon] Registry persistence detected: New service "WindowsUpdateHelper" created pointing to C:\\ProgramData\\update.exe. File signed with invalid certificate, established scheduled task for hourly execution.',
            'source': 'Sysmon',
            'severity': 'Alta',
            'timestamp': '2025-03-19 15:23:11',
            'metadata': {
                'service_name': 'WindowsUpdateHelper',    # Nome ingannevole
                'file_path': 'C:\\ProgramData\\update.exe',
                'persistence_type': 'Servizio + Attività Pianificata',  # Doppia persistenza
                'certificate': 'Non valido'
            },
            'explanation': 'Il malware che stabilisce persistenza tramite servizi e attività pianificate indica la fase di installazione',
            'phase': 'installation',
            'indicators': ['Creazione di servizio', 'Attività pianificata', 'Meccanismo di persistenza']
        },
        {
            'id': 'social_install_1',
            'raw': '2025-03-15 15:42:08 [ENDPOINT_PROTECTION] Rilevata installazione software non autorizzato su workstation WS-CONTA-07. Utente ha scaricato e installato "TeamViewer_Support.exe" dopo chiamata di supporto tecnico falso. Software legittimo usato per accesso remoto malevolo.',
            'source': 'Endpoint Protection',
            'severity': 'Alta',
            'timestamp': '2025-03-15 15:42:08',
            'metadata': {
                'workstation': 'WS-CONTA-07',
                'installed_software': 'TeamViewer_Support.exe',
                'installation_trigger': 'falso_supporto_tecnico',
                'software_type': 'remote_access_tool',
                'legitimate_software': True
            },
            'explanation': 'Installazione di software legittimo (TeamViewer) ottenuta tramite social engineering telefonico fingendosi supporto tecnico, creando backdoor per accesso remoto.',
            'phase': 'installation',
            'indicators': ['Installazione software remoto', 'Chiamata supporto falso', 'Software legittimo usato male']
        }
    ],
    
    # --- FASE 6: COMMAND & CONTROL ---
    # Log che mostrano comunicazioni C2
    'command_control': [
        {
            'id': 'c2_1',
            'raw': '2025-03-20 09:12:45 [Network Monitor] Suspicious beaconing detected: Host 10.0.1.45 communicating with 185.234.219.11:443 every 60 seconds with jitter of 10%. Traffic pattern matches Cobalt Strike beacon.',
            'source': 'Monitor di Sicurezza di Rete',
            'severity': 'Critica',
            'timestamp': '2025-03-20 09:12:45',
            'metadata': {
                'internal_host': '10.0.1.45',
                'c2_server': '185.234.219.11:443',
                'beacon_interval': '60 secondi',   # Intervallo regolare tipico di C2
                'protocol': 'HTTPS'                # Usa protocollo legittimo per mimetizzarsi
            },
            'explanation': 'Un pattern regolare di beaconing verso un server esterno indica l\'avvenuta creazione di un canale di comando e controllo.',
            'phase': 'command_control',
            'indicators': ['Comportamento di beaconing', 'Intervalli regolari', 'Comunicazione esterna']
        },
        {
            'id': 'social_c2_1',
            'raw': '2025-03-15 17:15:29 [NETWORK_MONITORING] Stabilita connessione outbound persistente verso remote-support.tech-solutions.org:443 da workstation WS-CONTA-07. Traffico criptato su porta HTTPS ma pattern insolito. Utente continua a ricevere "istruzioni di supporto" via telefono.',
            'source': 'Network Monitoring',
            'severity': 'Critica',
            'timestamp': '2025-03-15 17:15:29',
            'metadata': {
                'c2_server': 'remote-support.tech-solutions.org',
                'source_workstation': 'WS-CONTA-07',
                'connection_port': 443,
                'traffic_encrypted': True,
                'ongoing_phone_support': True
            },
            'explanation': 'Establishment di canale comando e controllo mascherato da sessione di supporto tecnico remoto, con attaccante che mantiene comunicazione vocale per istruzioni.',
            'phase': 'command_control',
            'indicators': ['Connessione outbound persistente', 'Traffico C2 mascherato', 'Supporto telefonico continuativo']
        }
    ],
    
    # --- FASE 7: ACTIONS ON OBJECTIVES ---
    # Log che mostrano il raggiungimento degli obiettivi finali
    'actions_objectives': [
        {
            'id': 'action_1',
            'raw': '2025-03-21 14:45:33 [DLP] Mass data exfiltration detected: 15GB of sensitive files from Finance share compressed and uploaded to cloud storage. Files include "Q1_Financial_Report.xlsx", "Customer_Database.csv".',
            'source': 'Prevenzione Perdita Dati',
            'severity': 'Critica',
            'timestamp': '2025-03-21 14:45:33',
            'metadata': {
                'data_volume': '15GB',                    # Grande volume indica esfiltrazione
                'file_types': ['Report finanziari', 'Dati clienti'],
                'destination': 'Cloud storage',
                'compression': True                       # Compressi per eludere DLP
            },
            'explanation': 'Il furto su larga scala di dati indica che l\'attaccante ha raggiunto l\'obiettivo di sottrarre informazioni sensibili.',
            'phase': 'actions_objectives',
            'indicators': ['Esfiltrazione di dati', 'File sensibili', 'Grande volume di dati']
        },
        {
            'id': 'social_actions_1',
            'raw': '2025-03-15 19:33:52 [DLP] Tentativo di esfiltrazione massiva file contabili bloccato. Utente laura.bianchi@company.local tentava upload di 847 file Excel su servizio cloud esterno dopo istruzioni ricevute via telefono da presunto "auditor esterno". Trasferimento interrotto dopo 12MB.',
            'source': 'Data Loss Prevention',
            'severity': 'Critica',
            'timestamp': '2025-03-15 19:33:52',
            'metadata': {
                'user': 'laura.bianchi@company.local',
                'files_count': 847,
                'file_type': 'Excel_contabili',
                'upload_destination': 'cloud_esterno',
                'social_pretext': 'audit_esterno',
                'data_transferred': '12MB'
            },
            'explanation': 'Tentativo di esfiltrazione dati contabili attraverso inganno sociale con impersonificazione di auditor esterno, sfruttando la fiducia nell\'autorità.',
            'phase': 'actions_objectives',
            'indicators': ['Esfiltrazione dati massiva', 'Impersonificazione auditor', 'Upload cloud non autorizzato']
        }
    ]
}

# ============================================================================
# STRATEGIE DI MITIGAZIONE PER OGNI FASE
# Contromisure reali utilizzate nell'industry per ogni fase della kill chain
# ============================================================================

MITIGATION_STRATEGIES = {
    # Mitigazioni per la fase di ricognizione
    'reconnaissance': [
        {
            'id': 'recon_mit_1',
            'name': 'Riduzione della Superficie d\'Attacco',
            'description': 'Limitare i servizi e le informazioni esposte pubblicamente',
            'icon': '🛡️',
            'effectiveness': 'Alta'
        },
        {
            'id': 'recon_mit_2',
            'name': 'Monitoraggio DNS',
            'description': 'Monitorare e segnalare query DNS sospette',
            'icon': '🔍',
            'effectiveness': 'Alta'
        },
        {
            'id': 'social_recon_mit_1',
            'name': 'Formazione Consapevolezza Sociale',
            'description': 'Educare staff su tecniche di social engineering e procedure di verifica dell\'identità',
            'icon': '🧠',
            'effectiveness': 'Alta'
        }
    ],
    
    # Mitigazioni per la fase di armamento
    'weaponization': [
        {
            'id': 'weapon_mit_1',
            'name': 'Feed di Threat Intelligence',
            'description': 'Sottoscrivere feed di IOC per rilevare malware noto',
            'icon': '📰',
            'effectiveness': 'Alta'
        },
        {
            'id': 'weapon_mit_2',
            'name': 'Analisi in Sandbox',
            'description': 'Analizzare file sospetti in un ambiente isolato',
            'icon': '📦',
            'effectiveness': 'Alta'
        },
        {
            'id': 'social_weapon_mit_1',
            'name': 'Verifica Mittente Multipla',
            'description': 'Implementare controlli SPF/DKIM e training su verifica identità mittente',
            'icon': '✅',
            'effectiveness': 'Alta'
        }
    ],
    
    # Mitigazioni per la fase di consegna
    'delivery': [
        {
            'id': 'delivery_mit_1',
            'name': 'Gateway di Sicurezza Email',
            'description': 'Filtrare email e allegati dannosi',
            'icon': '📧',
            'effectiveness': 'Alta'
        },
        {
            'id': 'delivery_mit_2',
            'name': 'Lista Bianca delle Applicazioni',
            'description': 'Consentire l\'esecuzione solo ad applicazioni approvate',
            'icon': '✅',
            'effectiveness': 'Molto Alta'  # Efficacia massima
        },
        {
            'id': 'social_delivery_mit_1',
            'name': 'Processo Doppia Autorizzazione',
            'description': 'Richiedere conferma telefonica per trasferimenti finanziari e modifiche critiche',
            'icon': '🔐',
            'effectiveness': 'Molto Alta'
        }
    ],
    
    # Mitigazioni per la fase di sfruttamento
    'exploitation': [
        {
            'id': 'exploit_mit_1',
            'name': 'Gestione delle Patch',
            'description': 'Applicare immediatamente le patch di sicurezza',
            'icon': '🔄',
            'effectiveness': 'Molto Alta'
        },
        {
            'id': 'exploit_mit_2',
            'name': 'Soluzione EDR',
            'description': 'Implementare soluzioni di rilevamento e risposta sugli endpoint',
            'icon': '💻',
            'effectiveness': 'Alta'
        },
        {
            'id': 'social_exploit_mit_1',
            'name': 'Autenticazione Multi-Fattore',
            'description': 'Implementare MFA per tutti gli accessi e educare su phishing SMS/call',
            'icon': '🔑',
            'effectiveness': 'Molto Alta'
        }
    ],
    
    # Mitigazioni per la fase di installazione
    'installation': [
        {
            'id': 'install_mit_1',
            'name': 'Controllo delle Applicazioni',
            'description': 'Impedire l\'installazione di software non autorizzato',
            'icon': '🚫',
            'effectiveness': 'Molto Alta'
        },
        {
            'id': 'install_mit_2',
            'name': 'Monitoraggio dell\'Integrità dei File',
            'description': 'Rilevare modifiche non autorizzate ai file di sistema',
            'icon': '📁',
            'effectiveness': 'Alta'
        },
        {
            'id': 'social_install_mit_1',
            'name': 'Controllo Installazioni Software',
            'description': 'Bloccare installazioni non autorizzate e definire processo supporto tecnico verificato',
            'icon': '🚫',
            'effectiveness': 'Alta'
        }
    ],
    
    # Mitigazioni per la fase di comando e controllo
    'command_control': [
        {
            'id': 'c2_mit_1',
            'name': 'Analisi del Traffico di Rete',
            'description': 'Rilevare connessioni in uscita anomale',
            'icon': '📡',
            'effectiveness': 'Alta'
        },
        {
            'id': 'c2_mit_2',
            'name': 'DNS Sinkholing',
            'description': 'Reindirizzare i domini dannosi verso un server interno',
            'icon': '🕳️',
            'effectiveness': 'Alta'
        },
        {
            'id': 'social_c2_mit_1',
            'name': 'Monitoraggio Connessioni Anomale',
            'description': 'Detectare traffico C2 insolito e stabilire protocolli supporto tecnico autenticati',
            'icon': '📡',
            'effectiveness': 'Alta'
        }
    ],
    
    # Mitigazioni per la fase di azioni sugli obiettivi
    'actions_objectives': [
        {
            'id': 'action_mit_1',
            'name': 'Backup e Ripristino dei Dati',
            'description': 'Mantenere backup offline per il ripristino da ransomware',
            'icon': '💾',
            'effectiveness': 'Molto Alta'
        },
        {
            'id': 'action_mit_2',
            'name': 'Soluzioni DLP',
            'description': 'Impedire l\'esfiltrazione non autorizzata di dati',
            'icon': '🔒',
            'effectiveness': 'Alta'
        },
        {
            'id': 'social_actions_mit_1',
            'name': 'Prevenzione Perdita Dati (DLP)',
            'description': 'Implementare DLP per trasferimenti massivi e procedure verifica per audit esterni',
            'icon': '🛡️',
            'effectiveness': 'Molto Alta'
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
        'phases': list(LOGS_AND_SE_DATABASE.keys()),  # Tutte e 7 le fasi
        'time_limit': 30,          # Solo 30 secondi per rispondere
        'base_points': 50          # Massimo punteggio per esperti
    }
}