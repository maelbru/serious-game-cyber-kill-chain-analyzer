"""
CYBER KILL CHAIN ANALYZER - FLASK APP (SECURED VERSION)
Versione sicura con rate limiting, CORS e validazione input
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Import dei nostri moduli
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
# FLASK APP INITIALIZATION
# ============================================================================

load_dotenv()
app = Flask(__name__)

# ✅ CORS SICURO - Solo origini autorizzate
allowed_origins = [
    "http://localhost:5173",    # Vite dev server
    "http://127.0.0.1:5173",    # Alternativa localhost
    "http://localhost:3000",    # Create React App fallback
]

# In produzione, usa variabile d'ambiente
if os.getenv('FLASK_ENV') == 'production':
    frontend_url = os.getenv('FRONTEND_URL')
    if frontend_url:
        allowed_origins = [frontend_url]

CORS(app, 
     origins=allowed_origins,
     methods=['GET', 'POST'],           # Solo metodi necessari
     allow_headers=['Content-Type'],    # Solo headers necessari
     supports_credentials=False         # No cookies per sicurezza
)

# ✅ RATE LIMITER
limiter = create_limiter(app)

# Configurazione logging migliorata
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# MIDDLEWARE E ERROR HANDLERS
# ============================================================================

@app.before_request
def before_request():
    """Middleware eseguito prima di ogni richiesta"""
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """Middleware eseguito dopo ogni richiesta"""
    # Headers di sicurezza
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Rate-Limit-Info'] = 'Check headers for limits'
    return response

@app.errorhandler(404)
def not_found(error):
    """Handler per errori 404"""
    return jsonify(format_api_response(False, error="Endpoint not found")), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handler per errori 405"""
    return jsonify(format_api_response(False, error="Method not allowed")), 405

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handler per rate limit exceeded"""
    logger.warning(f"Rate limit exceeded for {request.remote_addr}")
    return jsonify(format_api_response(
        False, 
        error="Rate limit exceeded. Troppi tentativi, riprova più tardi."
    )), 429

@app.errorhandler(500)
def internal_error(error):
    """Handler per errori 500"""
    logger.error(f"Internal server error: {error}")
    return jsonify(format_api_response(False, error="Internal server error")), 500

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/api/health', methods=['GET'])
@limiter.limit("30 per minute")  # Limite specifico per health check
def health_check():
    """Endpoint di health check con informazioni sistema"""
    try:
        health_data = {
            'status': 'healthy',
            'timestamp': get_current_timestamp(),
            'game': 'Cyber Kill Chain Analyzer',
            'version': '1.0.2',  # Incrementata per versione sicura
            'active_sessions': GameService.get_session_count(),
            'security': 'enabled'
        }
        
        return jsonify(format_api_response(True, health_data))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "health_check")), 500

# ============================================================================
# GAME DATA ENDPOINTS
# ============================================================================

@app.route('/api/get-phases', methods=['GET'])
@limiter.limit("60 per minute")
def get_phases():
    """Ottiene tutte le fasi della Cyber Kill Chain"""
    try:
        phases = GameService.get_all_phases()
        return jsonify(format_api_response(True, {'phases': phases}))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "get_phases")), 500

@app.route('/api/leaderboard', methods=['GET'])
@limiter.limit("30 per minute")
def get_leaderboard():
    """Ottiene la classifica globale"""
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(max(1, limit), 50)  # Limita tra 1 e 50
        
        leaderboard = GameService.get_global_leaderboard(limit)
        return jsonify(format_api_response(True, {'leaderboard': leaderboard}))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "get_leaderboard")), 500

# ============================================================================
# GAME LOGIC ENDPOINTS - CON VALIDAZIONE E RATE LIMITING
# ============================================================================

@app.route('/api/get-log', methods=['POST'])
@limiter.limit("20 per minute", key_func=get_user_key)  # 20 log per minuto per utente
@validate_json_input(SessionDataSchema)  # ✅ VALIDAZIONE AUTOMATICA
def get_log(validated_data):
    """Ottiene un nuovo log di sicurezza da analizzare"""
    try:
        session_id = validated_data['session_id']
        difficulty = validated_data['difficulty']
        stats = validated_data['stats']
        
        logger.info(f"Generating log for session {session_id[:8]}... difficulty {difficulty}")
        
        # Genera nuovo log tramite servizio
        result = GameService.generate_log(session_id, difficulty, stats)
        
        return jsonify(format_api_response(True, result))
        
    except ValueError as e:
        logger.warning(f"ValueError in get_log: {e}")
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        return jsonify(handle_api_error(e, "get_log")), 500

@app.route('/api/validate-phase', methods=['POST'])
@limiter.limit("30 per minute", key_func=get_user_key)  # 30 validazioni per minuto
@validate_json_input(PhaseValidationSchema)  # ✅ VALIDAZIONE AUTOMATICA
def validate_phase(validated_data):
    """Valida la fase della Cyber Kill Chain selezionata"""
    try:
        session_id = validated_data['session_id']
        selected_phase = validated_data['selected_phase']
        
        logger.info(f"Validating phase {selected_phase} for session {session_id[:8]}...")
        
        # Valida tramite servizio
        result = GameService.validate_phase_selection(session_id, selected_phase)
        
        return jsonify(format_api_response(True, result))
        
    except ValueError as e:
        logger.warning(f"ValueError in validate_phase: {e}")
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        return jsonify(handle_api_error(e, "validate_phase")), 500

@app.route('/api/validate-mitigation', methods=['POST'])
@limiter.limit("30 per minute", key_func=get_user_key)  # 30 validazioni per minuto
@validate_json_input(MitigationValidationSchema)  # ✅ VALIDAZIONE AUTOMATICA
def validate_mitigation(validated_data):
    """Valida la strategia di mitigazione selezionata"""
    try:
        session_id = validated_data['session_id']
        selected_mitigation = validated_data['selected_mitigation']
        time_remaining = validated_data['time_remaining']
        difficulty = validated_data['difficulty']
        
        logger.info(f"Validating mitigation {selected_mitigation} for session {session_id[:8]}...")
        
        # Valida tramite servizio
        result = GameService.validate_mitigation_selection(
            session_id, selected_mitigation, time_remaining, difficulty
        )
        
        # Aggiorna statistiche sessione
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
# STATISTICS ENDPOINTS
# ============================================================================

@app.route('/api/statistics', methods=['POST'])
@limiter.limit("60 per minute", key_func=get_user_key)
def get_statistics():
    """Ottiene le statistiche dell'utente"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default') if data else 'default'
        
        stats = GameService.get_session_statistics(session_id)
        return jsonify(format_api_response(True, stats))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "get_statistics")), 500

@app.route('/api/reset-session', methods=['POST'])
@limiter.limit("10 per minute", key_func=get_user_key)  # Limite basso per reset
def reset_session():
    """Resetta una sessione utente"""
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
# MAINTENANCE ENDPOINTS (ADMIN) - CON RATE LIMITING STRETTO
# ============================================================================

@app.route('/api/admin/cleanup-sessions', methods=['POST'])
@limiter.limit("5 per hour")  # Limite molto basso per admin
def cleanup_sessions():
    """Pulisce le sessioni vecchie - solo per admin"""
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
# STARTUP LOGIC
# ============================================================================

def initialize_app():
    """Inizializza l'applicazione con controlli di sicurezza"""
    logger.info("=== CYBER KILL CHAIN ANALYZER - SECURE VERSION ===")
    logger.info("Starting backend with security features enabled...")
    
    # Verifica configurazioni critiche
    if os.getenv('FLASK_ENV') == 'production':
        logger.info("✅ Production mode detected")
        if not os.getenv('FRONTEND_URL'):
            logger.warning("⚠️  FRONTEND_URL not set in production!")
    else:
        logger.info("🔧 Development mode")
    
    logger.info(f"✅ CORS allowed origins: {allowed_origins}")
    logger.info("✅ Rate limiting enabled")
    logger.info("✅ Input validation enabled")
    logger.info("✅ Security headers enabled")
    logger.info(f"✅ Game phases loaded: {len(GameService.get_all_phases())}")
    logger.info("🛡️  Backend initialization complete - SECURED")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    initialize_app()
    
    # Configurazione sicura per sviluppo
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(
        debug=debug_mode,
        port=5000,
        host='127.0.0.1'  # Solo localhost per sicurezza
    )