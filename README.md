# 🛡️ Cyber Kill Chain Analyzer

Questo progetto è una webapp educativa basata su React e Flask che integra un sistema di gamification per imparare la **Cyber Kill Chain**.

È progettato per analizzare log di sicurezza reali e identificare le fasi degli attacchi informatici, valutando automaticamente secondo le migliori pratiche di **cybersecurity**.

## 🚀 Caratteristiche principali

- ✅ **Webapp in React** con interfaccia intuitiva e moderna
- 🧠 **Backend Flask** con API RESTful per la gestione del gioco
- 🎯 **Sistema di gamification** ottimizzato per l'apprendimento della cybersecurity
- 📊 **Analisi log realistici** con feedback contestuale e coerente
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
│   │   └── helpers.py            # Utility functions e validazione
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
2. **📋 Analizza i Log**: Leggi attentamente i log di sicurezza presentati
3. **🎯 Identifica la Fase**: Seleziona la fase corretta della Cyber Kill Chain
4. **🛡️ Scegli la Mitigazione**: Se corretto, seleziona la strategia di difesa ottimale
5. **📈 Accumula Punti**: Guadagna punti in base a velocità e precisione
6. **🏆 Sblocca Achievement**: Raggiungi traguardi e migliora le tue competenze

### Fasi della Cyber Kill Chain

1. **🔍 Reconnaissance** - Raccolta informazioni sul target
2. **🔨 Weaponization** - Creazione del payload malevolo
3. **📧 Delivery** - Consegna del malware al target
4. **💥 Exploitation** - Sfruttamento delle vulnerabilità
5. **⚙️ Installation** - Installazione del malware
6. **📡 Command & Control** - Controllo remoto del sistema
7. **🎯 Actions on Objectives** - Raggiungimento degli obiettivi

## 🔧 Configurazione

### Variabili Environment

Il progetto utilizza configurazioni predefinite, ma puoi personalizzare:

- **Backend Port**: Modifica in `app.py` (default: 5000)
- **API Timeout**: Modifica in `frontend/src/utils/constants.js`
- **Difficoltà**: Configurabile in `backend/models/game_data.py`

### Modalità Debug

Per abilitare il debug completo:

```bash
# Backend
export FLASK_DEBUG=1
python app.py

# Frontend
npm run dev -- --debug
```

## 📊 API Endpoints

### Game Management
- `POST /api/get-log` - Ottiene un nuovo log da analizzare
- `POST /api/validate-phase` - Valida la fase selezionata
- `POST /api/validate-mitigation` - Valida la strategia di mitigazione

### Statistics & Info
- `GET /api/get-phases` - Lista delle fasi Kill Chain
- `POST /api/statistics` - Statistiche utente
- `GET /api/leaderboard` - Classifica globale
- `GET /api/health` - Health check del sistema

## 🎯 Funzionalità Avanzate

- **🧠 AI-Driven Difficulty**: Algoritmo che adatta la difficoltà dinamicamente
- **📱 Progressive Web App**: Installabile su dispositivi mobili
- **🔄 Offline Mode**: Funziona completamente offline con dati di fallback
- **♿ Accessibility**: Supporto completo per screen reader e navigazione keyboard
- **🎨 Dark Theme**: Design moderno con tema scuro e animazioni fluide

## 📝 Roadmap

- [ ] **Database persistente** per statistiche utente
- [ ] **Modalità multiplayer** con competizioni in tempo reale
- [ ] **Integrazione MITRE ATT&CK** framework
- [ ] **Machine Learning** per personalizzazione log
- [ ] **Mobile app** nativa iOS/Android
- [ ] **Plugin browser** per analisi log live

## 🐛 Bug Report & Feature Request

Per segnalare bug o richiedere nuove funzionalità, apri una issue su GitHub con:
- Descrizione dettagliata del problema/feature
- Passaggi per riprodurre (per bug)
- Screenshot se necessario
- Informazioni su browser/OS

## 📜 License

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🙏 Ringraziamenti

- **Lockheed Martin** per il framework Cyber Kill Chain
- **MITRE Corporation** per ATT&CK framework
- **Symbiotic AI** per le linee guida di cybersecurity education
- **React Team** per l'eccellente framework frontend
- **Flask Community** per il micro-framework backend

---