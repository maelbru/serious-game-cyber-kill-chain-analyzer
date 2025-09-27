# 🛡️ Cyber Kill Chain Analyzer

Questo progetto è una webapp educativa basata su React e Flask che integra un sistema di gamification per imparare la **Cyber Kill Chain**.

È progettato per analizzare log di sicurezza reali e **tecniche di social engineering**, identificando le fasi degli attacchi informatici e valutando automaticamente secondo le migliori pratiche di **cybersecurity**.

## 🚀 Caratteristiche principali

- ✅ **Webapp in React** 
- 🧠 **Backend Flask** con API RESTful per la gestione del gioco
- 🎯 **Sistema di gamification** ottimizzato per l'apprendimento della cybersecurity
- 📊 **Analisi log realistici** con feedback contestuale e coerente
- 🎭 **Riconoscimento Social Engineering** - Identifica tecniche di ingegneria sociale
- 📞 **Scenari telefonic/email phishing** - Casi reali di attacchi BEC e vishing
- ⚡ **Difficoltà dinamica** che si adatta alle performance dell'utente
- 🏆 **Sistema di achievements** con progressione e statistiche dettagliate
- 📱 **Design responsive** compatibile con tutti i dispositivi
- 🔄 **Modalità offline** per funzionamento senza connessione backend

## 📂 Struttura del progetto

```
cyber-kill-chain-analyzer/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── services/
│   │   └── game_service.py       # Business logic del gioco
│   ├── models/
│   │   └── game_data.py          # Dati statici e configurazione
│   ├── utils/
│   │   ├── helpers.py            # Utility functions e validazione
│   │   ├── rate_limiter.py       # Rate limiting configuration
│   │   └── validators.py         # Input validation schemas
│   ├── requirements.txt          # Dipendenze Python
│   └── venv/                     # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Componente principale React
│   │   ├── components/          # Componenti UI modulari
│   │   ├── hooks/               # Custom hooks per la logica
│   │   ├── utils/               # Costanti e utility
│   │   └── App.css              # Stili personalizzati e design system
│   ├── package.json             # Dipendenze Node.js
│   └── vite.config.js           # Configurazione build tool
└── README.md                    # Questo file
```

## 🛠️ Clonare la repository

```bash
git clone https://github.com/tuousername/cyber-kill-chain-analyzer.git
cd cyber-kill-chain-analyzer
```

## 🔧 Setup e Installazione

### Backend (Flask)

1. **Creare virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Attivare virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installare dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Avviare il server**:
   ```bash
   python app.py
   ```
   Il backend sarà disponibile su `http://localhost:5000`

### Frontend (React)

1. **Installare dipendenze**:
   ```bash
   cd frontend
   npm install
   ```

2. **Avviare in modalità sviluppo**:
   ```bash
   npm run dev
   ```
   Il frontend sarà disponibile su `http://localhost:5173`

3. **Build per produzione**:
   ```bash
   npm run build
   ```

## 🎮 Come Giocare

1. **📚 Tutorial**: Inizia con il tutorial per capire le meccaniche di gioco
2. **📋 Analizza la Situazione**: Leggi attentamente i log di sicurezza presentati o gli scenari di social engineering
3. **🎯 Identifica la Fase**: Seleziona la fase corretta della Cyber Kill Chain
4. **🛡️ Scegli la Mitigazione**: Se corretto, seleziona la strategia di difesa ottimale
5. **📈 Accumula Punti**: Guadagna punti in base a velocità e precisione

### 🎭 Tipologie di Scenari

Il gioco include diversi tipi di attacchi da analizzare:

#### **📊 Log di Sicurezza Tecnici**
- Log di rete (IDS/IPS)
- Log di sicurezza email
- Log di endpoint security
- Log di firewall e proxy

#### **📞 Attacchi di Social Engineering**
- **Vishing** (Voice Phishing): Chiamate telefoniche fraudolente
- **Email Phishing**: Email di phishing mirate
- **BEC** (Business Email Compromise): Impersonificazione CEO/dirigenti
- **Pretexting**: Scenari di impersonificazione tecnica
- **Baiting**: Esca tramite supporti rimovibili o download

### Fasi della Cyber Kill Chain

1. **🔍 Reconnaissance** - Raccolta informazioni sul target (include OSINT e social engineering)
2. **🔨 Weaponization** - Creazione del payload malevolo (include documenti con social engineering)
3. **📧 Delivery** - Consegna del malware al target (include campagne phishing)
4. **💥 Exploitation** - Sfruttamento delle vulnerabilità (include manipolazione umana)
5. **⚙️ Installation** - Installazione del malware (include installazioni "assistite")
6. **📡 Command & Control** - Controllo remoto del sistema (include canali mascherati)
7. **🎯 Actions on Objectives** - Raggiungimento degli obiettivi (include esfiltrazione sociale)

## 📊 API Endpoints

### Game Management
- `POST /api/get-log` - Ottiene un nuovo log da analizzare (tecnico o social engineering)
- `POST /api/validate-phase` - Valida la fase selezionata
- `POST /api/validate-mitigation` - Valida la strategia di mitigazione

### Statistics & Info
- `GET /api/get-phases` - Lista delle fasi Kill Chain
- `GET /api/health` - Health check del sistema

### Security Features
- `POST /api/reset-session` - Reset sessione utente
- `POST /api/admin/cleanup-sessions` - Pulizia sessioni (admin)
- `GET /api/admin/stats` - Statistiche sistema (admin)

## 🎯 Funzionalità Avanzate

### 🧠 AI-Driven Difficulty
Algoritmo che adatta la difficoltà dinamicamente basandosi su:
- Precisione delle risposte
- Velocità di risposta
- Serie di successi consecutivi
- Tipologia di errori commessi

### 🎭 Social Engineering Detection
- **Riconoscimento Pattern**: Identifica tecniche comuni di manipolazione
- **Analisi Psicologica**: Comprende i trigger emotivi utilizzati
- **Contromisure Umane**: Suggerisce strategie di difesa comportamentali
- **Awareness Training**: Migliora la consapevolezza sulle tecniche sociali

### 📱 Progressive Web App
- Funziona completamente offline con dati di fallback

---

💡 **Nota**: Questo progetto è puramente educativo e tutti gli scenari di social engineering sono simulati per scopi didattici. Utilizzare queste conoscenze solo per difesa e mai per attacchi reali.
