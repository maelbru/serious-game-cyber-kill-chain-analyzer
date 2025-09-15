"""
CYBER KILL CHAIN ANALYZER - GAME SERVICE
Contiene tutta la logica di business del gioco educativo
"""

import random
import logging
from models.game_data import (
    LOGS_DATABASE, 
    MITIGATION_STRATEGIES, 
    CYBER_KILL_CHAIN_PHASES,
    DIFFICULTY_CONFIG
)
from utils.helpers import (
    validate_session_data,
    validate_difficulty,
    validate_phase,
    validate_stats,
    calculate_difficulty_level,
    calculate_points,
    calculate_time_limit,
    sanitize_log_data,
    get_current_timestamp,
    log_user_action,
    get_effectiveness_score
)

logger = logging.getLogger(__name__)

# ============================================================================
# GESTIONE DELLE SESSIONI UTENTE
# ============================================================================

# Dizionario che mantiene i dati di tutte le sessioni utente in memoria
# TODO: verrà sostituito da un database
user_sessions = {}

class GameService:
    """
    Classe principale che gestisce tutta la logica del gioco (tutti i metodi sono statici)
    """
    
    @staticmethod
    def get_or_create_session(session_id):
        """
        Ottiene una sessione esistente o ne crea una nuova
        
        Args:
            session_id (str): Identificatore univoco della sessione
            
        Returns:
            dict: Dati della sessione con statistiche e stato del gioco
        """
        # Se la sessione non esiste, viene creata con i valori di default
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'score': 0,                             # Punteggio totale accumulato
                'streak': 0,                            # Serie di risposte corrette consecutive
                'total_attempts': 0,                    # Numero totale di tentativi
                'correct_attempts': 0,                  # Numero di risposte corrette
                'current_log': None,                    # ID del log attualmente in gioco
                'correct_phase': None,                  # Fase corretta per il log corrente
                'correct_mitigation': None,             # Mitigazione ottimale per la fase
                'log_data': {},                         # Dati completi del log corrente
                'created_at': get_current_timestamp()   # Quando è stata creata la sessione
            }
            logger.info(f"Created new session: {session_id}")
        
        return user_sessions[session_id]
    
    @staticmethod
    def generate_log(session_id, difficulty='beginner', stats=None):
        """
        Genera un nuovo log di sicurezza per l'analisi da parte del giocatore
        
        Args:
            session_id (str): ID della sessione
            difficulty (str): Livello di difficoltà richiesto
            stats (dict): Statistiche attuali del giocatore per calcolo difficoltà dinamica
            
        Returns:
            dict: Contiene il log da analizzare, tempo limite e difficoltà effettiva
        """
        try:
            # Valida e pulisce i parametri di input
            difficulty = validate_difficulty(difficulty)
            stats = validate_stats(stats or {})
            
            # Ottieni o crea la sessione per questo utente
            session = GameService.get_or_create_session(session_id)
            
            # Calcola la difficoltà dinamica basata sulle performance
            if stats:
                dynamic_difficulty = calculate_difficulty_level(
                    stats['score'], stats['streak'], stats['accuracy']
                )
                # Usa la difficoltà più alta tra quella richiesta e quella calcolata
                if dynamic_difficulty == 'expert' or (dynamic_difficulty == 'intermediate' and difficulty == 'beginner'):
                    difficulty = dynamic_difficulty
            
            # Ottieni le fasi disponibili per questo livello di difficoltà
            available_phases = DIFFICULTY_CONFIG[difficulty]['phases']
            
            # Filtra i log disponibili basandosi sulle fasi permesse
            available_logs = []
            for phase in available_phases:
                if phase in LOGS_DATABASE:
                    available_logs.extend(LOGS_DATABASE[phase])
            
            # Verifica che ci siano log disponibili
            if not available_logs:
                raise ValueError("No logs available for difficulty level")
            
            # Seleziona casualmente un log dalla lista disponibile
            selected_log = random.choice(available_logs)
            selected_phase = selected_log['phase']
            
            # Salva i dati nella sessione per la validazione futura
            session['current_log'] = selected_log['id']
            session['correct_phase'] = selected_phase
            session['log_data'] = selected_log
            
            # Calcola il tempo limite basato sulla difficoltà
            time_limit = calculate_time_limit(difficulty)
            
            # Rimuove informazioni sensibili dal log prima di inviarlo al client
            client_log = sanitize_log_data(selected_log)
            
            # Registra l'azione per debugging e analytics
            log_user_action(session_id, 'log_generated', {
                'log_id': selected_log['id'],
                'difficulty': difficulty,
                'phase': selected_phase
            })
            
            return {
                'log': client_log,
                'time_limit': time_limit,
                'difficulty': difficulty
            }
            
        except Exception as e:
            logger.error(f"Error generating log for session {session_id}: {e}")
            raise
    
    @staticmethod
    def validate_phase_selection(session_id, selected_phase):
        """
        Valida la selezione della fase Kill Chain
        
        Args:
            session_id (str): ID della sessione
            selected_phase (str): Fase selezionata dall'utente
            
        Returns:
            dict: Risultato della validazione
        """
        try:
            # Valida che la fase selezionata sia valida
            if not validate_phase(selected_phase):
                raise ValueError(f"Invalid phase: {selected_phase}")
            
            # Ottieni i dati della sessione
            session = GameService.get_or_create_session(session_id)
            correct_phase = session.get('correct_phase')
            log_data = session.get('log_data', {})
            
            # Verifica che ci sia un log attivo da validare
            if not correct_phase:
                raise ValueError("No active log to validate")
            
            # Controlla se la risposta è corretta
            is_correct = selected_phase == correct_phase
            
            if is_correct:
                # RISPOSTA CORRETTA - Prepara le strategie di mitigazione
                mitigation_options = MITIGATION_STRATEGIES.get(correct_phase, [])
                
                # Seleziona la mitigazione ottimale come "risposta corretta"
                if mitigation_options:
                    best_mitigation = max(
                        mitigation_options, 
                        key=lambda m: get_effectiveness_score(m['effectiveness'])
                    )
                    session['correct_mitigation'] = best_mitigation['id']
                
                # Registra il successo
                log_user_action(session_id, 'phase_correct', {
                    'selected_phase': selected_phase,
                    'log_id': session.get('current_log')
                })
                
                return {
                    'is_correct': True,
                    'mitigation_strategies': mitigation_options,
                    'explanation': log_data.get('explanation', ''),
                    'indicators': log_data.get('indicators', [])
                }
            else:
                # RISPOSTA SBAGLIATA - Fornisci feedback educativo
                phase_info = CYBER_KILL_CHAIN_PHASES.get(correct_phase, {})
                
                # Registra l'errore
                log_user_action(session_id, 'phase_incorrect', {
                    'selected_phase': selected_phase,
                    'correct_phase': correct_phase,
                    'log_id': session.get('current_log')
                })
                
                return {
                    'is_correct': False,
                    'correct_phase': correct_phase,
                    'phase_info': phase_info,
                    'explanation': log_data.get('explanation', ''),
                    'indicators': log_data.get('indicators', [])
                }
                
        except Exception as e:
            logger.error(f"Error validating phase for session {session_id}: {e}")
            raise
    
    @staticmethod
    def validate_mitigation_selection(session_id, selected_mitigation, time_remaining, difficulty):
        """
        Valida la strategia di mitigazione scelta dall'utente e calcola i punti
        
        Args:
            session_id (str): ID della sessione
            selected_mitigation (str): ID della mitigazione selezionata
            time_remaining (int): Secondi rimanenti quando ha risposto
            difficulty (str): Livello di difficoltà del round
            
        Returns:
            dict: Risultato con punti guadagnati e feedback sulla scelta
        """
        try:
            # Valida e pulisce i parametri
            difficulty = validate_difficulty(difficulty)
            time_remaining = max(0, int(time_remaining))
            
            # Ottieni i dati della sessione
            session = GameService.get_or_create_session(session_id)
            correct_phase = session.get('correct_phase')
            
            # Verifica che ci sia una fase attiva
            if not correct_phase:
                raise ValueError("No active phase to validate mitigation")
            
            # Trova le mitigazioni disponibili per questa fase
            phase_mitigations = MITIGATION_STRATEGIES.get(correct_phase, [])
            selected_mit_data = next(
                (m for m in phase_mitigations if m['id'] == selected_mitigation), 
                None
            )
            
            # Verifica che la mitigazione selezionata sia valida
            if not selected_mit_data:
                raise ValueError(f"Invalid mitigation: {selected_mitigation}")
            
            # Valuta l'efficacia della scelta (High e Very High sono considerate corrette)
            is_correct = selected_mit_data['effectiveness'] in ['High', 'Very High']
            
            # Calcola i punti basandosi su difficoltà, velocità e correttezza
            points = calculate_points(difficulty, time_remaining, True, is_correct)
            
            # Trova la mitigazione ottimale per confronto
            best_mitigation = None
            correct_mitigation_id = session.get('correct_mitigation')
            if correct_mitigation_id:
                best_mitigation = next(
                    (m for m in phase_mitigations if m['id'] == correct_mitigation_id),
                    None
                )
            
            # Registra il risultato per analytics
            log_user_action(session_id, 'mitigation_validated', {
                'selected_mitigation': selected_mitigation,
                'is_correct': is_correct,
                'points': points,
                'time_remaining': time_remaining,
                'effectiveness': selected_mit_data['effectiveness']
            })
            
            return {
                'is_correct': is_correct,
                'points': points,
                'selected_effectiveness': selected_mit_data['effectiveness'],
                'best_mitigation': best_mitigation
            }
            
        except Exception as e:
            logger.error(f"Error validating mitigation for session {session_id}: {e}")
            raise
    
    @staticmethod
    def get_session_statistics(session_id):
        """
        Calcola e restituisce le statistiche attuali della sessione
        
        Args:
            session_id (str): ID della sessione
            
        Returns:
            dict: Statistiche complete della sessione utente
        """
        try:
            session = GameService.get_or_create_session(session_id)
            
            # Ottieni i dati grezzi dalla sessione
            total_attempts = session.get('total_attempts', 0)
            correct_attempts = session.get('correct_attempts', 0)
            
            # Calcola la percentuale di accuratezza
            accuracy = 100.0
            if total_attempts > 0:
                accuracy = round((correct_attempts / total_attempts) * 100, 2)
            
            return {
                'total_games': total_attempts,                    # Partite totali giocate
                'correct_answers': correct_attempts,              # Risposte corrette
                'current_score': session.get('score', 0),         # Punteggio totale
                'current_streak': session.get('streak', 0),       # Serie corrente
                'accuracy': accuracy,                             # Percentuale accuratezza
                'session_created': session.get('created_at', '')  # Quando è iniziata 
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics for session {session_id}: {e}")
            raise
    
    @staticmethod
    def update_session_stats(session_id, points, is_correct):
        """
        Aggiorna le statistiche della sessione dopo ogni round
        
        Args:
            session_id (str): ID della sessione
            points (int): Punti da aggiungere al punteggio
            is_correct (bool): Se l'ultima risposta era corretta
            
        Returns:
            dict: Statistiche aggiornate della sessione
        """
        try:
            session = GameService.get_or_create_session(session_id)
            
            # Aggiorna il punteggio totale
            session['score'] = session.get('score', 0) + points
            
            # Incrementa il contatore dei tentativi totali
            session['total_attempts'] = session.get('total_attempts', 0) + 1
            
            # Gestisci streak e risposte corrette
            if is_correct:
                session['correct_attempts'] = session.get('correct_attempts', 0) + 1 
                session['streak'] = session.get('streak', 0) + 1 # Incrementa la serie
            else:
                session['streak'] = 0 # Reset della serie se sbagliato
            
            # Registra l'aggiornamento per debugging
            log_user_action(session_id, 'stats_updated', {
                'points_added': points,
                'is_correct': is_correct,
                'new_score': session['score'],
                'new_streak': session['streak']
            })
            
            # Restituisce le statistiche aggiornate
            return GameService.get_session_statistics(session_id)
            
        except Exception as e:
            logger.error(f"Error updating stats for session {session_id}: {e}")
            raise
    
    @staticmethod
    def get_global_leaderboard(limit=10):
        """
        Restituisce la classifica globale dei migliori giocatori
        
        Args:
            limit (int): Numero massimo di giocatori da restituire
            
        Returns:
            list: Lista dei migliori giocatori con rank, nome, score e livello di competenza
            
        Note:
            Attualmente usa dati mock per demo. In produzione dovrebbe
            interrogare un database reale con i punteggi degli utenti.
        """
        try:
            # Mock data per demo - in produzione userebbe un database reale
            mock_leaderboard = [
                {'rank': 1, 'name': 'CyberHunter', 'score': 2150, 'mastery': '7/7 phases'},
                {'rank': 2, 'name': 'SecurityPro', 'score': 1890, 'mastery': '6/7 phases'},
                {'rank': 3, 'name': 'KillChainMaster', 'score': 1750, 'mastery': '7/7 phases'},
                {'rank': 4, 'name': 'ThreatAnalyst', 'score': 1620, 'mastery': '5/7 phases'},
                {'rank': 5, 'name': 'BlueTeamer', 'score': 1500, 'mastery': '4/7 phases'},
                {'rank': 6, 'name': 'SOCAnalyst', 'score': 1350, 'mastery': '5/7 phases'},
                {'rank': 7, 'name': 'InfoSecPro', 'score': 1200, 'mastery': '4/7 phases'},
                {'rank': 8, 'name': 'CyberDefender', 'score': 1100, 'mastery': '3/7 phases'},
                {'rank': 9, 'name': 'SecurityNinja', 'score': 950, 'mastery': '4/7 phases'},
                {'rank': 10, 'name': 'ThreatHunter', 'score': 850, 'mastery': '3/7 phases'}
            ]
            
            # Restituisce solo il numero richiesto di risultati
            return mock_leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            raise
    
    @staticmethod
    def get_all_phases():
        """
        Restituisce tutte le fasi della Cyber Kill Chain con i loro dettagli
        
        Returns:
            list: Lista di tutte le 7 fasi con ID, nome, descrizione e icona
        """
        try:
            phases = []
            for phase_id, phase_data in CYBER_KILL_CHAIN_PHASES.items():
                phases.append({
                    'id': phase_id,
                    'name': phase_data['name'],
                    'description': phase_data['description'],
                    'icon': phase_data['icon']
                })
            
            return phases
            
        except Exception as e:
            logger.error(f"Error getting phases: {e}")
            raise
    
    @staticmethod
    def reset_session(session_id):
        """
        Elimina completamente una sessione utente, resettando tutti i progressi
        
        Args:
            session_id (str): ID della sessione da eliminare
            
        Returns:
            bool: True se la sessione è stata eliminata con successo
        """
        try:
            # Verifica se la sessione esiste e la elimina
            if session_id in user_sessions:
                del user_sessions[session_id]
                log_user_action(session_id, 'session_reset', {})
                logger.info(f"Session {session_id} reset successfully")
                return True
            return False # Sessione non trovata
            
        except Exception as e:
            logger.error(f"Error resetting session {session_id}: {e}")
            raise
    
    @staticmethod
    def get_session_count():
        """
        Conta il numero di sessioni attualmente attive in memoria
        
        Returns:
            int: Numero totale di sessioni attive
        """
        return len(user_sessions)
    
    @staticmethod
    def cleanup_old_sessions(max_age_hours=24):
        """
        Rimuove le sessioni più vecchie di un certo tempo per liberare memoria
        
        Args:
            max_age_hours (int): Età massima delle sessioni in ore (default: 24)
            
        Returns:
            int: Numero di sessioni rimosse durante la pulizia
        """
        try:
            from datetime import datetime, timedelta
            
            # Calcola il timestamp di cutoff
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            sessions_to_remove = []
            
            # Trova tutte le sessioni troppo vecchie
            for session_id, session_data in user_sessions.items():
                created_at_str = session_data.get('created_at', '')
                if created_at_str:
                    try:
                        # Prova a parsare la data di creazione
                        created_at = datetime.fromisoformat(created_at_str)
                        if created_at < cutoff_time:
                            sessions_to_remove.append(session_id)
                    except ValueError:
                        # Se non riesce a parsare la data, è probabilmente corrotta
                        # quindi rimuovi la sessione per sicurezza
                        sessions_to_remove.append(session_id)
            
            # Rimuovi tutte le sessioni identificate
            for session_id in sessions_to_remove:
                del user_sessions[session_id]

            # Log del risultato se sono state rimosse sessioni    
            if sessions_to_remove:
                logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")
            
            return len(sessions_to_remove)
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
            return 0