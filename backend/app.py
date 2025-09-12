"""
CYBER KILL CHAIN ANALYZER - FLASK APP (REFACTORED)
Versione pulita con logica separata in servizi
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime

# Import dei nostri moduli
from services.game_service import GameService
from utils.helpers import (
    validate_session_data,
    format_api_response,
    handle_api_error,
    get_current_timestamp
)

# ============================================================================
# FLASK APP INITIALIZATION
# ============================================================================

app = Flask(__name__)
CORS(app)

# Configurazione logging
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
    # Log di tutte le richieste
    logger.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """Middleware eseguito dopo ogni richiesta"""
    # Aggiungi headers di sicurezza
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.errorhandler(404)
def not_found(error):
    """Handler per errori 404"""
    return jsonify(format_api_response(False, error="Endpoint not found")), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handler per errori 405"""
    return jsonify(format_api_response(False, error="Method not allowed")), 405

@app.errorhandler(500)
def internal_error(error):
    """Handler per errori 500"""
    logger.error(f"Internal server error: {error}")
    return jsonify(format_api_response(False, error="Internal server error")), 500

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint di health check con informazioni sistema"""
    try:
        health_data = {
            'status': 'healthy',
            'timestamp': get_current_timestamp(),
            'game': 'Cyber Kill Chain Analyzer',
            'version': '1.0.1',
            'active_sessions': GameService.get_session_count()
        }
        
        return jsonify(format_api_response(True, health_data))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "health_check")), 500

# ============================================================================
# GAME DATA ENDPOINTS
# ============================================================================

@app.route('/api/get-phases', methods=['GET'])
def get_phases():
    """Ottiene tutte le fasi della Cyber Kill Chain"""
    try:
        phases = GameService.get_all_phases()
        return jsonify(format_api_response(True, {'phases': phases}))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "get_phases")), 500

@app.route('/api/leaderboard', methods=['GET'])
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
# GAME LOGIC ENDPOINTS
# ============================================================================

@app.route('/api/get-log', methods=['POST'])
def get_log():
    """Ottiene un nuovo log di sicurezza da analizzare"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(format_api_response(False, error="No JSON data provided")), 400
        
        # Valida dati di sessione
        if not validate_session_data(data):
            return jsonify(format_api_response(False, error="Invalid session data")), 400
        
        session_id = data.get('session_id')
        difficulty = data.get('difficulty', 'beginner')
        stats = data.get('stats', {})
        
        # Genera nuovo log tramite servizio
        result = GameService.generate_log(session_id, difficulty, stats)
        
        return jsonify(format_api_response(True, result))
        
    except ValueError as e:
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        return jsonify(handle_api_error(e, "get_log")), 500

@app.route('/api/validate-phase', methods=['POST'])
def validate_phase():
    """Valida la fase della Cyber Kill Chain selezionata"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(format_api_response(False, error="No JSON data provided")), 400
        
        session_id = data.get('session_id')
        selected_phase = data.get('selected_phase')
        
        if not session_id or not selected_phase:
            return jsonify(format_api_response(False, error="Missing required fields")), 400
        
        # Valida tramite servizio
        result = GameService.validate_phase_selection(session_id, selected_phase)
        
        return jsonify(format_api_response(True, result))
        
    except ValueError as e:
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        return jsonify(handle_api_error(e, "validate_phase")), 500

@app.route('/api/validate-mitigation', methods=['POST'])
def validate_mitigation():
    """Valida la strategia di mitigazione selezionata"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(format_api_response(False, error="No JSON data provided")), 400
        
        session_id = data.get('session_id')
        selected_mitigation = data.get('selected_mitigation')
        time_remaining = data.get('time_remaining', 0)
        difficulty = data.get('difficulty', 'beginner')
        
        if not session_id or not selected_mitigation:
            return jsonify(format_api_response(False, error="Missing required fields")), 400
        
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
        return jsonify(format_api_response(False, error=str(e))), 400
    except Exception as e:
        return jsonify(handle_api_error(e, "validate_mitigation")), 500

# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@app.route('/api/statistics', methods=['POST'])
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
def reset_session():
    """Resetta una sessione utente"""
    try:
        data = request.get_json()
        if not data or not data.get('session_id'):
            return jsonify(format_api_response(False, error="Session ID required")), 400
        
        session_id = data.get('session_id')
        success = GameService.reset_session(session_id)
        
        if success:
            return jsonify(format_api_response(True, {'message': 'Session reset successfully'}))
        else:
            return jsonify(format_api_response(False, error="Session not found")), 404
        
    except Exception as e:
        return jsonify(handle_api_error(e, "reset_session")), 500

# ============================================================================
# MAINTENANCE ENDPOINTS (ADMIN)
# ============================================================================

@app.route('/api/admin/cleanup-sessions', methods=['POST'])
def cleanup_sessions():
    """Pulisce le sessioni vecchie - solo per admin"""
    try:
        # In produzione, aggiungere autenticazione admin qui
        max_age = request.json.get('max_age_hours', 24) if request.json else 24
        
        removed_count = GameService.cleanup_old_sessions(max_age)
        
        return jsonify(format_api_response(True, {
            'message': f'Cleaned up {removed_count} old sessions',
            'removed_count': removed_count,
            'remaining_sessions': GameService.get_session_count()
        }))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "cleanup_sessions")), 500

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    """Ottiene statistiche globali del sistema - solo per admin"""
    try:
        # In produzione, aggiungere autenticazione admin qui
        stats = {
            'active_sessions': GameService.get_session_count(),
            'server_uptime': get_current_timestamp(),
            'total_endpoints': 9,
            'health_status': 'healthy'
        }
        
        return jsonify(format_api_response(True, stats))
        
    except Exception as e:
        return jsonify(handle_api_error(e, "admin_stats")), 500

# ============================================================================
# STARTUP LOGIC
# ============================================================================

def initialize_app():
    """Inizializza l'applicazione"""
    logger.info("Starting Cyber Kill Chain Analyzer Backend...")
    logger.info(f"Game phases loaded: {len(GameService.get_all_phases())}")
    logger.info("Backend initialization complete")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    initialize_app()
    
    # Configurazione per sviluppo
    app.run(
        debug=True,
        port=5000,
        host='127.0.0.1'
    )