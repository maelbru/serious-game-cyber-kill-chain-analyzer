"""
CYBER KILL CHAIN ANALYZER - HELPER UTILITIES
Funzioni di supporto, validazione e calcoli
"""

import logging
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_session_data(data):
    """
    Valida i dati della sessione utente
    
    Args:
        data (dict): Dati della sessione da validare
        
    Returns:
        bool: True se i dati sono validi
    """
    if not isinstance(data, dict):
        return False
        
    required_fields = ['session_id']
    return all(field in data for field in required_fields)

def validate_difficulty(difficulty):
    """
    Valida il livello di difficoltà
    
    Args:
        difficulty (str): Livello di difficoltà
        
    Returns:
        str: Difficoltà validata o 'beginner' come default
    """
    valid_difficulties = ['beginner', 'intermediate', 'expert']
    return difficulty if difficulty in valid_difficulties else 'beginner'

def validate_phase(phase):
    """
    Valida che la fase sia una delle 7 fasi della Kill Chain
    
    Args:
        phase (str): Fase da validare
        
    Returns:
        bool: True se la fase è valida
    """
    valid_phases = [
        'reconnaissance', 'weaponization', 'delivery', 'exploitation',
        'installation', 'command_control', 'actions_objectives'
    ]
    return phase in valid_phases

def validate_stats(stats):
    """
    Valida le statistiche del giocatore
    
    Args:
        stats (dict): Statistiche da validare
        
    Returns:
        dict: Statistiche validate con valori di default
    """
    default_stats = {
        'score': 0,
        'streak': 0,
        'accuracy': 100
    }
    
    if not isinstance(stats, dict):
        return default_stats
        
    validated_stats = {}
    for key, default_value in default_stats.items():
        value = stats.get(key, default_value)
        # Assicura che i valori siano numerici e non negativi
        try:
            validated_stats[key] = max(0, float(value))
        except (ValueError, TypeError):
            validated_stats[key] = default_value
            
    return validated_stats

# ============================================================================
# CALCULATION FUNCTIONS
# ============================================================================

def calculate_difficulty_level(score, streak, accuracy):
    """
    Calcola il livello di difficoltà basato sulle performance
    
    Args:
        score (float): Punteggio attuale
        streak (int): Streak corrente
        accuracy (float): Percentuale di accuratezza
        
    Returns:
        str: Livello di difficoltà calcolato
    """
    try:
        performance_score = (score * 0.3) + (streak * 10) + (accuracy * 0.4)
        
        if performance_score < 50:
            return 'beginner'
        elif performance_score < 150:
            return 'intermediate'
        else:
            return 'expert'
    except (TypeError, ValueError) as e:
        logger.error(f"Error calculating difficulty: {e}")
        return 'beginner'

def calculate_points(difficulty, time_remaining, phase_correct, mitigation_correct):
    """
    Calcola i punti guadagnati in un round
    
    Args:
        difficulty (str): Livello di difficoltà
        time_remaining (int): Tempo rimanente in secondi
        phase_correct (bool): Se la fase è stata identificata correttamente
        mitigation_correct (bool): Se la mitigazione è corretta
        
    Returns:
        int: Punti guadagnati
    """
    try:
        base_points = {
            'beginner': 10,
            'intermediate': 25,
            'expert': 50
        }
        
        points = 0
        
        if phase_correct:
            points += base_points.get(difficulty, 10)
            
            if mitigation_correct:
                points += base_points.get(difficulty, 10)
                # Bonus tempo
                time_bonus = max(0, int(time_remaining * 0.5))
                points += time_bonus
        
        return max(0, points)
        
    except (TypeError, ValueError) as e:
        logger.error(f"Error calculating points: {e}")
        return 0

def calculate_time_limit(difficulty):
    """
    Calcola il tempo limite basato sulla difficoltà
    
    Args:
        difficulty (str): Livello di difficoltà
        
    Returns:
        int: Tempo limite in secondi
    """
    time_limits = {
        'beginner': 60,
        'intermediate': 40,
        'expert': 30
    }
    return time_limits.get(difficulty, 60)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_current_timestamp():
    """
    Ottiene il timestamp corrente in formato ISO
    
    Returns:
        str: Timestamp ISO formattato
    """
    return datetime.now().isoformat()

def sanitize_log_data(log_data):
    """
    Sanitizza i dati del log per la risposta API
    
    Args:
        log_data (dict): Dati del log originale
        
    Returns:
        dict: Dati sanitizzati per il client
    """
    if not isinstance(log_data, dict):
        return {}
        
    # Rimuove campi sensibili che non devono essere inviati al client
    sensitive_fields = ['explanation', 'phase', 'indicators']
    
    sanitized = {}
    for key, value in log_data.items():
        if key not in sensitive_fields:
            sanitized[key] = value
            
    return sanitized

def format_api_response(success=True, data=None, error=None):
    """
    Formatta una risposta API standardizzata
    
    Args:
        success (bool): Se la richiesta è andata a buon fine
        data (dict): Dati di risposta
        error (str): Messaggio di errore
        
    Returns:
        dict: Risposta formattata
    """
    response = {
        'success': success,
        'timestamp': get_current_timestamp()
    }
    
    if success and data:
        response.update(data)
    elif not success and error:
        response['error'] = error
        
    return response

def log_user_action(session_id, action, details=None):
    """
    Logga un'azione dell'utente per debugging/analytics
    
    Args:
        session_id (str): ID della sessione
        action (str): Tipo di azione
        details (dict): Dettagli aggiuntivi
    """
    log_entry = {
        'timestamp': get_current_timestamp(),
        'session_id': session_id,
        'action': action
    }
    
    if details:
        log_entry['details'] = details
        
    logger.info(f"User action: {log_entry}")

def get_effectiveness_score(effectiveness):
    """
    Converte l'efficacia testuale in punteggio numerico
    
    Args:
        effectiveness (str): Livello di efficacia
        
    Returns:
        int: Punteggio numerico (1-4)
    """
    effectiveness_map = {
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Very High': 4
    }
    return effectiveness_map.get(effectiveness, 1)

# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

def handle_api_error(error, context="Unknown"):
    """
    Gestisce e logga errori API
    
    Args:
        error (Exception): Errore da gestire
        context (str): Contesto dell'errore
        
    Returns:
        dict: Risposta di errore formattata
    """
    error_message = str(error)
    logger.error(f"API Error in {context}: {error_message}")
    
    # Non esporre dettagli tecnici al client
    if "database" in error_message.lower():
        client_message = "Errore di sistema temporaneo"
    elif "validation" in error_message.lower():
        client_message = "Dati non validi forniti"
    else:
        client_message = "Errore interno del server"
        
    return format_api_response(False, error=client_message)