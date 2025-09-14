"""
CYBER KILL CHAIN ANALYZER - HELPER UTILITIES
Funzioni di supporto per validazione, calcoli e utilità varie
"""

import logging
from datetime import datetime

# Configurazione del logging per questo modulo
logger = logging.getLogger(__name__)

# ============================================================================
# FUNZIONI DI VALIDAZIONE INPUT
# ============================================================================

def validate_session_data(data):
    """
    Verifica che i dati della sessione siano nel formato corretto
    
    Args:
        data (dict): Dati della sessione da validare
        
    Returns:
        bool: True se i dati sono validi, False altrimenti
    """
    # Controlla che sia un dizionario
    if not isinstance(data, dict):
        return False
    
    # Verifica che contenga tutti i campi obbligatori
    required_fields = ['session_id']
    return all(field in data for field in required_fields)

def validate_difficulty(difficulty):
    """
    Controlla che il livello di difficoltà sia valido e lo normalizza
    
    Args:
        difficulty (str): Livello di difficoltà da validare
        
    Returns:
        str: Difficoltà validata o 'beginner' come fallback sicuro
    """
    valid_difficulties = ['beginner', 'intermediate', 'expert']
    return difficulty if difficulty in valid_difficulties else 'beginner'

def validate_phase(phase):
    """
    Verifica che la fase sia una delle 7 fasi valide della Kill Chain
    
    Args:
        phase (str): Nome della fase da validare
        
    Returns:
        bool: True se la fase è valida, False altrimenti
    """
    valid_phases = [
        'reconnaissance',    # Ricognizione
        'weaponization',     # Preparazione armi
        'delivery',          # Consegna
        'exploitation',      # Sfruttamento
        'installation',      # Installazione
        'command_control',   # Comando e controllo
        'actions_objectives' # Azioni sugli obiettivi
    ]
    return phase in valid_phases

def validate_stats(stats):
    """
    Pulisce e valida le statistiche del giocatore, fornendo valori di default sicuri
    
    Args:
        stats (dict): Statistiche da validare
        
    Returns:
        dict: Statistiche validate con valori di default per campi mancanti
    """
    # Valori di default sicuri per le statistiche
    default_stats = {
        'score': 0,      # Punteggio totale
        'streak': 0,     # Serie di risposte corrette
        'accuracy': 100  # Percentuale di accuratezza
    }
    
    # Se non è un dizionario, usa i valori di default
    if not isinstance(stats, dict):
        return default_stats
    
    # Valida ogni campo individualmente
    validated_stats = {}
    for key, default_value in default_stats.items():
        value = stats.get(key, default_value)
        # Assicura che i valori siano numerici e non negativi
        try:
            validated_stats[key] = max(0, float(value))
        except (ValueError, TypeError):
            # Se non può convertire a numero, usa il valore di default
            validated_stats[key] = default_value
            
    return validated_stats

# ============================================================================
# FUNZIONI PER CALCOLI DI GIOCO
# ============================================================================

def calculate_difficulty_level(score, streak, accuracy):
    """
    Calcola dinamicamente il livello di difficoltà basato sulle performance del giocatore
    
    Args:
        score (float): Punteggio totale accumulato
        streak (int): Serie corrente di risposte corrette
        accuracy (float): Percentuale di accuratezza (0-100)
        
    Returns:
        str: Livello di difficoltà calcolato ('beginner', 'intermediate', 'expert')
    """
    try:
        # Formula che combina tutti i fattori di performance
        # Score ha peso 30%, streak 10 punti per unità, accuracy 40% del suo valore
        performance_score = (score * 0.3) + (streak * 10) + (accuracy * 0.4)
        
        # Soglie per determinare il livello
        if performance_score < 50:
            return 'beginner'     # Giocatore principiante
        elif performance_score < 150:
            return 'intermediate' # Giocatore intermedio
        else:
            return 'expert'       # Giocatore esperto
    except (TypeError, ValueError) as e:
        logger.error(f"Error calculating difficulty: {e}")
        return 'beginner'  # Fallback sicuro in caso di errore

def calculate_points(difficulty, time_remaining, phase_correct, mitigation_correct):
    """
    Calcola i punti guadagnati dal giocatore in un round
    
    Args:
        difficulty (str): Livello di difficoltà del round
        time_remaining (int): Secondi rimanenti quando ha risposto
        phase_correct (bool): Se ha identificato correttamente la fase
        mitigation_correct (bool): Se ha scelto una mitigazione efficace
        
    Returns:
        int: Punti totali guadagnati (sempre >= 0)
    """
    try:
        # Punti base per ogni livello di difficoltà
        base_points = {
            'beginner': 10,      # Facile = meno punti
            'intermediate': 25,  # Medio = punti medi
            'expert': 50        # Difficile = più punti
        }
        
        points = 0
        
        # Punti solo se ha identificato correttamente la fase
        if phase_correct:
            points += base_points.get(difficulty, 10)
            
            # Bonus aggiuntivo se anche la mitigazione è corretta
            if mitigation_correct:
                points += base_points.get(difficulty, 10)
                # Bonus extra per velocità di risposta
                time_bonus = max(0, int(time_remaining * 0.5))
                points += time_bonus
        
        return max(0, points)  # Assicura che i punti non siano mai negativi
        
    except (TypeError, ValueError) as e:
        logger.error(f"Error calculating points: {e}")
        return 0  # Nessun punto in caso di errore

def calculate_time_limit(difficulty):
    """
    Determina il tempo limite per rispondere basato sulla difficoltà
    
    Args:
        difficulty (str): Livello di difficoltà
        
    Returns:
        int: Tempo limite in secondi
    """
    time_limits = {
        'beginner': 60,      # 1 minuto per principianti
        'intermediate': 40,  # 40 secondi per livello intermedio
        'expert': 30        # 30 secondi per esperti
    }
    return time_limits.get(difficulty, 60)  # Default a 60 secondi se non trovato

# ============================================================================
# FUNZIONI DI UTILITÀ GENERALE
# ============================================================================

def get_current_timestamp():
    """
    Restituisce il timestamp corrente in formato ISO standard
    
    Returns:
        str: Timestamp nel formato YYYY-MM-DDTHH:MM:SS.ffffff
    """
    return datetime.now().isoformat()

def sanitize_log_data(log_data):
    """
    Rimuove informazioni sensibili dal log prima di inviarlo al frontend
    Questo previene che il client veda la risposta corretta prima di rispondere
    
    Args:
        log_data (dict): Dati completi del log dal database
        
    Returns:
        dict: Log pulito senza informazioni che rovinerebbero il gioco
    """
    if not isinstance(log_data, dict):
        return {}
    
    # Campi che contengono spoiler e vanno rimossi
    sensitive_fields = ['explanation', 'phase', 'indicators']
    
    # Crea una copia pulita del log
    sanitized = {}
    for key, value in log_data.items():
        if key not in sensitive_fields:
            sanitized[key] = value
            
    return sanitized

def format_api_response(success=True, data=None, error=None):
    """
    Crea una risposta API standardizzata per garantire consistenza
    
    Args:
        success (bool): Se l'operazione è riuscita
        data (dict): Dati da includere nella risposta (solo se success=True)
        error (str): Messaggio di errore (solo se success=False)
        
    Returns:
        dict: Risposta formattata secondo lo standard dell'API
    """
    # Struttura base della risposta
    response = {
        'success': success,
        'timestamp': get_current_timestamp()
    }
    
    # Aggiungi dati o errore a seconda del risultato
    if success and data:
        response.update(data)  # Aggiungi tutti i dati alla risposta
    elif not success and error:
        response['error'] = error
        
    return response

def log_user_action(session_id, action, details=None):
    """
    Registra un'azione dell'utente per debugging e analytics
    Utile per capire come i giocatori interagiscono con il gioco
    
    Args:
        session_id (str): ID della sessione che ha eseguito l'azione
        action (str): Tipo di azione eseguita
        details (dict): Dettagli aggiuntivi sull'azione (opzionale)
    """
    # Crea la struttura del log
    log_entry = {
        'timestamp': get_current_timestamp(),
        'session_id': session_id,
        'action': action
    }
    
    # Aggiungi dettagli se forniti
    if details:
        log_entry['details'] = details
        
    # Registra nel sistema di logging
    logger.info(f"User action: {log_entry}")

def get_effectiveness_score(effectiveness):
    """
    Converte il livello di efficacia testuale in un punteggio numerico
    per poter fare confronti e ordinamenti
    
    Args:
        effectiveness (str): Livello di efficacia testuale
        
    Returns:
        int: Punteggio numerico da 1 (basso) a 4 (molto alto)
    """
    effectiveness_map = {
        'Low': 1,        # Efficacia bassa
        'Medium': 2,     # Efficacia media
        'High': 3,       # Efficacia alta
        'Very High': 4   # Efficacia molto alta
    }
    return effectiveness_map.get(effectiveness, 1)  # Default a 1 se non trovato

# ============================================================================
# FUNZIONI PER GESTIONE ERRORI
# ============================================================================

def handle_api_error(error, context="Unknown"):
    """
    Gestisce e registra errori API in modo standardizzato
    Nasconde dettagli tecnici sensibili dal client per sicurezza
    
    Args:
        error (Exception): L'errore da gestire
        context (str): Contesto dove si è verificato l'errore
        
    Returns:
        dict: Risposta di errore formattata per il client
    """
    error_message = str(error)
    logger.error(f"API Error in {context}: {error_message}")
    
    # Nasconde dettagli tecnici dal client per sicurezza
    # Fornisce messaggi user-friendly basati sul tipo di errore
    if "database" in error_message.lower():
        client_message = "Errore di sistema temporaneo"
    elif "validation" in error_message.lower():
        client_message = "Dati non validi forniti"
    else:
        client_message = "Errore interno del server"
        
    return format_api_response(False, error=client_message)