"""
CYBER KILL CHAIN ANALYZER - FLASK APP 
Applicazione Flask sicura con rate limiting, validazione input e gestione errori
"""

# Importazioni per il framework Flask e utilità
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# # Importazione moduli personalizzati
from services.game_service import GameService
from utils.helpers import (
    validate_session_data,
    format_api_response,
    handle_api_error,
    get_current_timestamp
)
from utils.rate_limiter import create_limiter, get_user_key
from utils.validators import (
    SessionDataSchema, 
    PhaseValidationSchema, 
    MitigationValidationSchema,
    validate_json_input
)

# ============================================================================
# INIZIALIZZAZIONE FLASK
# ============================================================================

# Carica le variabili d'ambiente dal file .env
load_dotenv()
app = Flask(__name__)

# Configurazione CORS
# Permette solo alle origini specificate di fare richieste al backend
allowed_origins = [
    "http://localhost:5173",    # Server di sviluppo Vite
    "http://127.0.0.1:5173",    # Versione alternativa di localhost
    "http://localhost:3000",    # Create React App (backup)
]

# In produzione, usa l'URL del frontend dalle variabili d'ambiente
if os.getenv('FLASK_ENV') == 'production':
    frontend_url = os.getenv('FRONTEND_URL')
    if frontend_url:
        allowed_origins = [frontend_url]

# Configurazione CORS sicura - permette solo metodi e headers necessari
CORS(app, 
     origins=allowed_origins,           # Solo origini autorizzate
     methods=['GET', 'POST'],           # Solo metodi HTTP necessari
     allow_headers=['Content-Type'],    # Solo headers necessari
     supports_credentials=False         # Nessun cookie
)

# Rate Limiter
limiter = create_limiter(app)

# Configurazione logging migliorata
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# MIDDLEWARE E GESTORI DI ERRORE
# ============================================================================

@app.before_request
def before_request():
    """
    Middleware eseguito PRIMA di ogni richiesta
    Logga tutte le richieste in arrivo per monitoraggio
    
    """
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """
    Middleware eseguito DOPO ogni richiesta
    Aggiunge headers di sicurezza a tutte le risposte
    """
    # Headers di sicurezza per proteggere il browser
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Rate-Limit-Info'] = 'Check headers for limits'
    return response

# Gestori di errori HTTP personalizzati
@app.errorhandler(404)
def not_found(error):
    """Gestisce errori 404 - Endpoint non trovato"""
    return jsonify(format_api_response(False, error="Endpoint not found")), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Gestisce errori 405 - Metodo HTTP non permesso"""
    return jsonify(format_api_response(False, error="Method not allowed")), 405

@app.errorhandler(429)
def ratelimit_handler(e):
    """Gestisce errori 429 - Rate limit superato"""
    logger.warning(f"Rate limit exceeded for {request.remote_addr}")
    return jsonify(format_api_response(
        False, 
        error="Rate limit exceeded. Troppi tentativi, riprova più tardi."
    )), 429

@app.errorhandler(500)
def internal_error(error):
    """Gestisce errori 500 - Errori interni del server"""
    logger.error(f"Internal server error: {error}")
    return jsonify(format_api_response(False, error="Internal server error")), 500

# ============================================================================
# ENDPOINT DI MONITORAGGIO
# ============================================================================

@app.route('/api/health', methods=['GET'])
@limiter.limit("30 per minute")  # Limite specifico per questo endpoint
def health_check():
    """
    Endpoint di health check per verificare che il server sia funzionante
    Usato per monitoring e deployment 
    """
    try:
        health_data = {
            'status': 'healthy',                                    # Stato del server
            'timestamp': get_current_timestamp(),                   # Quando è stata fatta la richiesta
            'game': 'Cyber Kill Chain Analyzer',                    # Nome dell'applicazione
            'version': '1.0.2',                                     # Versione corrente
            'active_sessions': GameService.get_session_count(),     # Sessioni attive
            'security': 'enabled'                                   # Sicurezza attiva
        }
        
        return jsonify(format_api_response(True, health_data))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "health_check")), 500

# ============================================================================
# ENDPOINT PER DATI DEL GIOCO
# ============================================================================

@app.route('/api/get-phases', methods=['GET'])
@limiter.limit("60 per minute") # Limite più alto perché è solo lettura
def get_phases():
    """
    Restituisce tutte le fasi della Cyber Kill Chain
    Usato dal frontend per mostrare le opzioni disponibili
    """
    try:
        phases = GameService.get_all_phases()
        return jsonify(format_api_response(True, {'phases': phases}))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "get_phases")), 500

@app.route('/api/leaderboard', methods=['GET'])
@limiter.limit("30 per minute")
def get_leaderboard():
    """
    Restituisce la classifica globale dei giocatori
    Permette di specificare quanti risultati mostrare (max 50)
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(max(1, limit), 50)  # Limita tra 1 e 50
        
        leaderboard = GameService.get_global_leaderboard(limit)
        return jsonify(format_api_response(True, {'leaderboard': leaderboard}))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "get_leaderboard")), 500

# ============================================================================
# ENDPOINT PRINCIPALI DEL GIOCO - CON SICUREZZA E VALIDAZIONE
# ============================================================================

@app.route('/api/get-log', methods=['POST'])
@limiter.limit("20 per minute", key_func=get_user_key)  # 20 log per minuto per utente
@validate_json_input(SessionDataSchema)                 # Validazione automatica dell'input
def get_log(validated_data):
    """
    Genera un nuovo log di sicurezza per l'analisi
    
    Input richiesto:
    - session_id: ID univoco della sessione utente
    - difficulty: Livello di difficoltà (beginner/intermediate/expert)
    - stats: Statistiche attuali del giocatore
    
    Output:
    - log: Dati del log da analizzare
    - time_limit: Tempo limite per rispondere
    - difficulty: Difficoltà effettiva assegnata
    """
    try:
        # Estrae i dati validati dal decorator
        session_id = validated_data['session_id']
        difficulty = validated_data['difficulty']
        stats = validated_data['stats']
        
        # Log per debugging
        logger.info(f"Generating log for session {session_id[:8]}... difficulty {difficulty}")
        
        # Genera il nuovo log tramite il service
        result = GameService.generate_log(session_id, difficulty, stats)
        
        return jsonify(format_api_response(True, result))
        
    except ValueError as e:
        # Errori di validazione dei dati
        logger.warning(f"ValueError in get_log: {e}")
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        # Altri errori imprevisti
        return jsonify(handle_api_error(e, "get_log")), 500

@app.route('/api/validate-phase', methods=['POST'])
@limiter.limit("30 per minute", key_func=get_user_key)  # 30 validazioni per minuto
@validate_json_input(PhaseValidationSchema)  # Validazione automatica
def validate_phase(validated_data):
    """
    Valida la fase della Cyber Kill Chain selezionata dall'utente
    
    Input richiesto:
    - session_id: ID della sessione
    - selected_phase: Fase selezionata dall'utente
    
    Output:
    - is_correct: Se la risposta è corretta
    - mitigation_strategies: Strategie di mitigazione (se corretto)
    - explanation: Spiegazione della risposta
    - indicators: Indicatori chiave nel log
    """
    try:
        session_id = validated_data['session_id']
        selected_phase = validated_data['selected_phase']
        
        logger.info(f"Validating phase {selected_phase} for session {session_id[:8]}...")
        
        # Valida la risposta tramite il service
        result = GameService.validate_phase_selection(session_id, selected_phase)
        
        return jsonify(format_api_response(True, result))
        
    except ValueError as e:
        logger.warning(f"ValueError in validate_phase: {e}")
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        return jsonify(handle_api_error(e, "validate_phase")), 500

@app.route('/api/validate-mitigation', methods=['POST'])
@limiter.limit("30 per minute", key_func=get_user_key)  # 30 validazioni per minuto
@validate_json_input(MitigationValidationSchema)  # Validazione automatica
def validate_mitigation(validated_data):
    """
    Valida la strategia di mitigazione selezionata dall'utente
    
    Input richiesto:
    - session_id: ID della sessione
    - selected_mitigation: Mitigazione selezionata
    - time_remaining: Tempo rimanente quando ha risposto
    - difficulty: Livello di difficoltà
    
    Output:
    - is_correct: Se la mitigazione è efficace
    - points: Punti guadagnati
    - selected_effectiveness: Efficacia della scelta
    - best_mitigation: Mitigazione ottimale (se sbagliato)
    """
    try:
        session_id = validated_data['session_id']
        selected_mitigation = validated_data['selected_mitigation']
        time_remaining = validated_data['time_remaining']
        difficulty = validated_data['difficulty']
        
        logger.info(f"Validating mitigation {selected_mitigation} for session {session_id[:8]}...")
        
        # Valida la mitigazione
        result = GameService.validate_mitigation_selection(
            session_id, selected_mitigation, time_remaining, difficulty
        )
        
        # Aggiorna le statistiche della sessione
        GameService.update_session_stats(
            session_id, 
            result.get('points', 0), 
            result.get('is_correct', False)
        )
        
        return jsonify(format_api_response(True, result))
        
    except ValueError as e:
        logger.warning(f"ValueError in validate_mitigation: {e}")
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        return jsonify(handle_api_error(e, "validate_mitigation")), 500

# ============================================================================
# ENDPOINT PER STATISTICHE
# ============================================================================

@app.route('/api/statistics', methods=['POST'])
@limiter.limit("60 per minute", key_func=get_user_key)
def get_statistics():
    """
    Restituisce le statistiche dell'utente per la sessione corrente
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default') if data else 'default'
        
        stats = GameService.get_session_statistics(session_id)
        return jsonify(format_api_response(True, stats))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "get_statistics")), 500

@app.route('/api/reset-session', methods=['POST'])
@limiter.limit("10 per minute", key_func=get_user_key)  # Limite basso per i reset
def reset_session():
    """
    Resetta una sessione utente eliminando tutti i dati salvati
    """    
    try:
        data = request.get_json()
        if not data or not data.get('session_id'):
            return jsonify(format_api_response(False, error="Session ID required")), 400
        
        session_id = data.get('session_id')
        success = GameService.reset_session(session_id)
        
        if success:
            logger.info(f"Session {session_id[:8]}... reset successfully")
            return jsonify(format_api_response(True, {'message': 'Session reset successfully'}))
        else:
            return jsonify(format_api_response(False, error="Session not found")), 404
        
    except Exception as e:
        return jsonify(handle_api_error(e, "reset_session")), 500

# ============================================================================
# ENDPOINT DI AMMINISTRAZIONE - CON RATE LIMITING STRINGENTE
# ============================================================================

@app.route('/api/admin/cleanup-sessions', methods=['POST'])
@limiter.limit("5 per hour")  # Limite molto basso per operazioni admin
def cleanup_sessions():
    """
    Pulisce le sessioni vecchie per liberare memoria
    Dovrebbe essere usato solo dagli amministratori
    """
    try:
        # TODO: In produzione, aggiungere autenticazione admin
        max_age = request.json.get('max_age_hours', 24) if request.json else 24
        
        removed_count = GameService.cleanup_old_sessions(max_age)
        
        logger.info(f"Cleaned up {removed_count} old sessions")
        
        return jsonify(format_api_response(True, {
            'message': f'Cleaned up {removed_count} old sessions',
            'removed_count': removed_count,
            'remaining_sessions': GameService.get_session_count()
        }))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "cleanup_sessions")), 500

@app.route('/api/admin/stats', methods=['GET'])
@limiter.limit("10 per hour")  # Limite basso per admin stats
def admin_stats():
    """Ottiene statistiche globali del sistema - solo per admin"""
    try:
        # TODO: In produzione, aggiungere autenticazione admin
        stats = {
            'active_sessions': GameService.get_session_count(),
            'server_uptime': get_current_timestamp(),
            'total_endpoints': 11,  # Aggiornato
            'health_status': 'healthy',
            'security_features': [
                'CORS Protection',
                'Rate Limiting',
                'Input Validation',
                'Security Headers'
            ]
        }
        
        return jsonify(format_api_response(True, stats))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "admin_stats")), 500

# ============================================================================
# LOGICA DI AVVIO
# ============================================================================

def initialize_app():
    """
    Inizializza l'applicazione e verifica la configurazione
    """
    logger.info("=== CYBER KILL CHAIN ANALYZER ===")
    logger.info("Starting backend with security features enabled...")
    
    # Verifica configurazioni per produzione
    if os.getenv('FLASK_ENV') == 'production':
        logger.info("✅ Production mode detected")
        if not os.getenv('FRONTEND_URL'):
            logger.warning("⚠️  FRONTEND_URL not set in production!")
    else:
        logger.info("🔧 Development mode")
    
    # Log delle configurazioni di sicurezza
    logger.info(f"✅ CORS allowed origins: {allowed_origins}")
    logger.info("✅ Rate limiting enabled")
    logger.info("✅ Input validation enabled")
    logger.info("✅ Security headers enabled")
    logger.info(f"✅ Game phases loaded: {len(GameService.get_all_phases())}")
    logger.info("🛡️  Backend initialization complete - SECURED")

# ============================================================================
# PUNTO DI INGRESSO PRINCIPALE
# ============================================================================

if __name__ == '__main__':
    # Inizializza l'app e le sue configurazioni
    initialize_app()
    
    # Configurazione sicura per l'ambiente di sviluppo
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Avvia il server Flask
    app.run(
        debug=debug_mode, # Debug solo se esplicitamente abilitato
        port=5000,        # Porta standard
        host='127.0.0.1'  # Solo localhost per sicurezza
    )