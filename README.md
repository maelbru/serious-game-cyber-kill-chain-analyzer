# 🛡️ Cyber Kill Chain Analyzer

[![License: MIT](https://img.shields.io/badge/Licenza-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0%2B-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000.svg)](https://flask.palletsprojects.com/)

> Un serious game educativo per la formazione in cybersecurity attraverso il framework Cyber Kill Chain

## 📋 Indice

- [Informazioni](#informazioni)
- [Caratteristiche](#caratteristiche)
- [Demo](#demo)
- [Guida Rapida](#guida-rapida)
  - [Prerequisiti](#prerequisiti)
  - [Installazione](#installazione)
  - [Avvio Rapido](#avvio-rapido)
- [Come Giocare](#come-giocare)
- [Architettura](#architettura)
- [Documentazione API](#documentazione-api)
- [Sviluppo](#sviluppo)
- [Testing](#testing)
- [Deployment](#deployment)
- [Dati di Ricerca](#dati-di-ricerca)
- [Contribuire](#contribuire)

## 🎯 Informazioni

**Cyber Kill Chain Analyzer** è un serious game educativo progettato per la formazione e la ricerca in cybersecurity. I giocatori analizzano log di sicurezza reali per identificare le fasi di attacco secondo il framework Cyber Kill Chain di Lockheed Martin e selezionare strategie di mitigazione appropriate.

### Contesto di Ricerca

Questo progetto è stato sviluppato come parte di una tesi sperimentale sulla gamification nell'educazione alla cybersecurity. Il gioco raccoglie metriche di performance per analizzare i pattern di apprendimento e l'efficacia degli approcci formativi basati sul gioco.

### Obiettivi Principali

- 🎓 **Educativo**: Insegnare le 7 fasi della Cyber Kill Chain attraverso esempi pratici
- 🎮 **Coinvolgente**: Elementi di gamification per mantenere interesse e motivazione
- 📊 **Misurabile**: Raccolta di dati quantitativi per l'analisi della ricerca
- 🔄 **Adattivo**: Difficoltà dinamica basata sulle performance del giocatore

## ✨ Caratteristiche

### Gameplay Principale
- **Analisi dei Log**: Log di sicurezza reali da varie fonti (IDS/IPS, EDR, SIEM)
- **Identificazione delle Fasi**: Riconoscere quale delle 7 fasi della Cyber Kill Chain rappresenta un attacco
- **Selezione della Mitigazione**: Scegliere la strategia più efficace per interrompere la catena di attacco
- **Difficoltà Adattiva**: Tre livelli (Principiante, Intermedio, Esperto) che si adattano automaticamente

### Elementi Educativi
- **Tutorial Interattivo**: Onboarding completo per nuovi giocatori
- **Feedback Immediato**: Spiegazioni dettagliate per risposte corrette e errate
- **Evidenziazione degli Indicatori**: Gli indicatori chiave dell'attacco vengono spiegati dopo ogni round
- **Tracciamento dei Progressi**: Monitorare i miglioramenti attraverso le diverse fasi di attacco

### Gamification
- **Sistema di Punteggio**: Punteggio basato su accuratezza e tempo di risposta
- **Bonus Streak**: Ricompense per risposte corrette consecutive
- **Progressione di Livello**: Sblocca scenari più complessi migliorando le competenze
- **Sistema Achievement**: Badge per il raggiungimento di traguardi
- **Classifica**: Confronta le performance con altri giocatori

## 🎮 Demo

### Screenshot

<details>
<summary>Visualizza Screenshot</summary>

#### Schermata di Benvenuto
![Schermata di Benvenuto](docs/images/welcome.png)

#### Tutorial
![Tutorial](docs/images/tutorial.png)

#### Gameplay
![Gameplay](docs/images/gameplay.png)

#### Selezione Mitigazione
![Mitigazione](docs/images/mitigation.png)

</details>

### Demo Live

🔗 [Prova la demo live](https://your-demo-url.com)

**Credenziali Demo:**
- Nessun login richiesto
- Progressi salvati localmente

## 🚀 Guida Rapida

### Prerequisiti

- **Python** 3.8 o superiore
- **Node.js** 18.0 o superiore
- **npm** o **yarn**
- **Git**

### Installazione

1. **Clona il repository**
```bash
git clone https://github.com/yourusername/cyber-kill-chain-analyzer.git
cd cyber-kill-chain-analyzer
```

2. **Setup Backend**
```bash
# Naviga nella directory backend
cd backend

# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente virtuale
# Su Windows:
venv\Scripts\activate
# Su macOS/Linux:
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

3. **Setup Frontend**
```bash
# Naviga nella directory frontend
cd ../frontend

# Installa dipendenze
npm install
# oppure
yarn install
```

### Avvio Rapido

1. **Avvia il Server Backend**
```bash
# Dalla directory backend con venv attivato
cd backend
python app.py
```
Il backend sarà disponibile su `http://localhost:5000`

2. **Avvia il Server di Sviluppo Frontend**
```bash
# Dalla directory frontend (nuovo terminale)
cd frontend
npm run dev
# oppure
yarn dev
```
Il frontend sarà disponibile su `http://localhost:5173`

3. **Accedi al Gioco**
Apri il browser e naviga su `http://localhost:5173`

## 🎯 Come Giocare

### Flusso di Gioco

1. **Schermata di Benvenuto**: Introduzione al gioco
2. **Tutorial**: Impara le fasi della Cyber Kill Chain e le meccaniche di gioco
3. **Analisi del Log**: Leggi e analizza il log di sicurezza presentato
4. **Selezione della Fase**: Identifica quale fase della Cyber Kill Chain rappresenta l'attacco
5. **Scelta della Mitigazione**: Se corretto, seleziona la strategia di mitigazione più efficace
6. **Feedback**: Ricevi punti e feedback educativo
7. **Progressione**: Continua al prossimo log con difficoltà adattata

### Le 7 Fasi della Cyber Kill Chain

| Fase | Icona | Descrizione | Indicatori Esempio |
|------|-------|-------------|-------------------|
| **Reconnaissance** | 🔍 | Raccolta informazioni sul target | Enumerazione DNS, port scanning |
| **Weaponization** | 🔨 | Creazione del payload malevolo | Creazione malware, packaging exploit |
| **Delivery** | 📧 | Trasmissione dell'arma al target | Email phishing, link malevoli |
| **Exploitation** | 💥 | Esecuzione del codice exploit | Process injection, sfruttamento vulnerabilità |
| **Installation** | ⚙️ | Installazione del malware | Meccanismi di persistenza, modifiche registro |
| **Command & Control** | 📡 | Controllo remoto del sistema | Beaconing, DNS tunneling |
| **Actions on Objectives** | 🎯 | Raggiungimento obiettivi attaccante | Esfiltrazione dati, deployment ransomware |

### Sistema di Punteggio

| Difficoltà | Punti Base | Bonus Tempo | Bonus Streak |
|------------|------------|-------------|--------------|
| Principiante | 10 pts | +0.5/sec | +5 per streak |
| Intermedio | 25 pts | +0.5/sec | +10 per streak |
| Esperto | 50 pts | +0.5/sec | +20 per streak |

## 🏗️ Architettura

### Panoramica del Sistema

```
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│  React Frontend │────▶│  Flask Backend  │
│                 │     │                 │
└─────────────────┘     └─────────────────┘
        │                       │
        │                       │
        ▼                       ▼
  [Local Storage]         [Session Store]
```

### Stack Tecnologico

#### Frontend
- **React** 18.x - Framework UI
- **Vite** - Build tool e dev server
- **Axios** - Client HTTP
- **CSS3** - Styling con custom properties

#### Backend
- **Flask** 3.0.0 - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Python** 3.8+ - Logica backend

### Struttura del Progetto

```
cyber-kill-chain-analyzer/
├── backend/
│   ├── app.py              # Applicazione Flask principale
│   ├── requirements.txt    # Dipendenze Python
│   └── venv/              # Ambiente virtuale (non nel repo)
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Componente React principale
│   │   ├── App.css        # Stili
│   │   └── main.jsx       # Entry point
│   ├── package.json       # Dipendenze Node
│   └── vite.config.js     # Configurazione Vite
├── docs/
│   ├── images/           # Screenshot
│   └── research/         # Documentazione ricerca
├── README.md
└── LICENSE
```

## 📡 Documentazione API

### URL Base
```
http://localhost:5000/api
```

### Endpoint

#### `GET /api/health`
Endpoint di health check

**Risposta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-03-15T10:30:00Z",
  "game": "Cyber Kill Chain Analyzer"
}
```

#### `POST /api/get-log`
Ottieni un nuovo log di sicurezza da analizzare

**Richiesta:**
```json
{
  "session_id": "user_abc123",
  "difficulty": "beginner",
  "stats": {
    "score": 150,
    "streak": 3,
    "accuracy": 85
  }
}
```

**Risposta:**
```json
{
  "log": {
    "id": "recon_1",
    "raw": "2024-03-15 09:23:17 [IDS] Multiple DNS queries...",
    "source": "Network IDS",
    "severity": "Medium",
    "timestamp": "2024-03-15 09:23:17",
    "metadata": {...}
  },
  "time_limit": 90
}
```

#### `POST /api/validate-phase`
Valida la fase della Cyber Kill Chain selezionata

**Richiesta:**
```json
{
  "session_id": "user_abc123",
  "selected_phase": "reconnaissance"
}
```

**Risposta:**
```json
{
  "is_correct": true,
  "mitigation_strategies": [...],
  "explanation": "Le query DNS multiple indicano la fase di reconnaissance...",
  "indicators": ["Enumerazione DNS", "Scansione esterna"]
}
```

#### `POST /api/validate-mitigation`
Valida la strategia di mitigazione selezionata

**Richiesta:**
```json
{
  "session_id": "user_abc123",
  "selected_mitigation": "dns_monitoring",
  "time_remaining": 45,
  "difficulty": "beginner"
}
```

**Risposta:**
```json
{
  "is_correct": true,
  "points": 35,
  "selected_effectiveness": "High",
  "best_mitigation": {...}
}
```

## 🔧 Sviluppo

### Setup Ambiente

1. **Variabili d'Ambiente Backend**
Crea file `.env` nella directory backend:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
PORT=5000
```

2. **Variabili d'Ambiente Frontend**
Crea file `.env` nella directory frontend:
```env
VITE_API_URL=http://localhost:5000/api
VITE_APP_ENV=development
```

### Stile del Codice

#### Python (Backend)
- Segui le linee guida PEP 8
- Usa type hints dove appropriato
- Lunghezza massima linea: 100 caratteri

#### JavaScript (Frontend)
- Configurazione ESLint fornita
- Prettier per la formattazione
- Usa componenti funzionali con hooks

### Aggiungere Nuovi Contenuti

#### Aggiungere Nuovi Log
Modifica `backend/app.py`:
```python
LOGS_DATABASE['nome_fase'].append({
    'id': 'id_univoco',
    'raw': 'Contenuto del log...',
    'source': 'Nome sistema',
    'severity': 'Low|Medium|High|Critical',
    'correctMitre': 'nome_fase',
    'explanation': 'Spiegazione educativa...',
    'indicators': ['indicatore1', 'indicatore2']
})
```

#### Aggiungere Strategie di Mitigazione
Modifica `backend/app.py`:
```python
MITIGATION_STRATEGIES['nome_fase'].append({
    'id': 'id_strategia',
    'name': 'Nome Strategia',
    'description': 'Descrizione...',
    'icon': '🛡️',
    'effectiveness': 'High|Medium|Low'
})
```

## 🧪 Testing

### Testing Backend
```bash
cd backend
python -m pytest tests/
```

### Testing Frontend
```bash
cd frontend
npm test
# oppure
yarn test
```

### Checklist Testing Manuale
- [ ] Il flusso del tutorial funziona correttamente
- [ ] I log si caricano senza errori
- [ ] La selezione della fase si valida correttamente
- [ ] Le strategie di mitigazione appaiono quando la fase è corretta
- [ ] I punti si calcolano correttamente
- [ ] La difficoltà si adatta in base alle performance
- [ ] Il design responsive funziona su mobile

## 🚢 Deployment

### Build di Produzione

#### Backend
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Frontend
```bash
cd frontend
npm run build
# oppure
yarn build
```
I file saranno generati in `frontend/dist/`

### Deployment Docker

```dockerfile
# Esempio Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Configurazione Ambiente

Per la produzione, assicurati che:
- Le impostazioni CORS siano configurate per il tuo dominio
- HTTPS sia abilitato
- Il rate limiting API sia implementato
- La gestione delle sessioni usi cookie sicuri
- La persistenza del database sia configurata

## 📊 Dati di Ricerca

### Metriche Raccolte

Il gioco raccoglie le seguenti metriche per scopi di ricerca:

- **Metriche di Performance**
  - Accuratezza per fase
  - Distribuzione del tempo di risposta
  - Progressione della curva di apprendimento
  - Pattern di errori comuni

- **Metriche di Coinvolgimento**
  - Durata della sessione
  - Numero di round giocati
  - Achievement di streak
  - Progressione della difficoltà

- **Metriche Educative**
  - Accuratezza nel riconoscimento delle fasi
  - Comprensione dell'efficacia delle strategie di mitigazione
  - Miglioramento nel tempo
  - Ritenzione delle conoscenze (giocatori che ritornano)

### Esportazione Dati

I dati di ricerca possono essere esportati tramite:
```bash
cd backend
python export_data.py --format csv --output dati_ricerca.csv
```

### Considerazioni sulla Privacy

- Tutti i dati sono anonimizzati
- Nessuna informazione personale viene raccolta
- Gli ID di sessione sono generati casualmente
- I dati sono salvati localmente per impostazione predefinita

---