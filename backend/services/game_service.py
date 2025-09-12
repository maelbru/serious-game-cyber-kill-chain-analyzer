"""
CYBER KILL CHAIN ANALYZER - GAME SERVICE
Tutta la business logic del gioco
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
# SESSION MANAGEMENT
# ============================================================================

# In-memory storage per le sessioni utente
user_sessions = {}

class GameService:
    """Servizio principale per la logica del gioco"""
    
    @staticmethod
    def get_or_create_session(session_id):
        """
        Ottiene o crea una sessione utente
        
        Args:
            session_id (str): ID della sessione
            
        Returns:
            dict: Dati della sessione
        """
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'score': 0,
                'streak': 0,
                'total_attempts': 0,
                'correct_attempts': 0,
                'current_log': None,
                'correct_phase': None,
                'correct_mitigation': None,
                'log_data': {},
                'created_at': get_current_timestamp()
            }
            logger.info(f"Created new session: {session_id}")
        
        return user_sessions[session_id]
    
    @staticmethod
    def generate_log(session_id, difficulty='beginner', stats=None):
        """
        Genera un nuovo log di sicurezza per l'analisi
        
        Args:
            session_id (str): ID della sessione
            difficulty (str): Livello di difficoltà
            stats (dict): Statistiche attuali del giocatore
            
        Returns:
            dict: Log generato e configurazione
        """
        try:
            # Valida input
            difficulty = validate_difficulty(difficulty)
            stats = validate_stats(stats or {})
            
            # Ottieni sessione
            session = GameService.get_or_create_session(session_id)
            
            # Calcola difficoltà dinamica se necessario
            if stats:
                dynamic_difficulty = calculate_difficulty_level(
                    stats['score'], stats['streak'], stats['accuracy']
                )
                # Usa la difficoltà più alta tra quella richiesta e quella calcolata
                if dynamic_difficulty == 'expert' or (dynamic_difficulty == 'intermediate' and difficulty == 'beginner'):
                    difficulty = dynamic_difficulty
            
            # Seleziona fasi disponibili per la difficoltà
            available_phases = DIFFICULTY_CONFIG[difficulty]['phases']
            
            # Filtra i log disponibili
            available_logs = []
            for phase in available_phases:
                if phase in LOGS_DATABASE:
                    available_logs.extend(LOGS_DATABASE[phase])
            
            if not available_logs:
                raise ValueError("No logs available for difficulty level")
            
            # Seleziona log casuale
            selected_log = random.choice(available_logs)
            selected_phase = selected_log['phase']
            
            # Salva nella sessione
            session['current_log'] = selected_log['id']
            session['correct_phase'] = selected_phase
            session['log_data'] = selected_log
            
            # Calcola tempo limite
            time_limit = calculate_time_limit(difficulty)
            
            # Sanitizza log per il client
            client_log = sanitize_log_data(selected_log)
            
            # Log azione utente
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
            # Valida input
            if not validate_phase(selected_phase):
                raise ValueError(f"Invalid phase: {selected_phase}")
            
            # Ottieni sessione
            session = GameService.get_or_create_session(session_id)
            correct_phase = session.get('correct_phase')
            log_data = session.get('log_data', {})
            
            if not correct_phase:
                raise ValueError("No active log to validate")
            
            is_correct = selected_phase == correct_phase
            
            if is_correct:
                # Fase corretta - prepara strategie di mitigazione
                mitigation_options = MITIGATION_STRATEGIES.get(correct_phase, [])
                
                # Seleziona mitigazione ottimale per la sessione
                if mitigation_options:
                    # Scegli la mitigazione con efficacia più alta come "corretta"
                    best_mitigation = max(
                        mitigation_options, 
                        key=lambda m: get_effectiveness_score(m['effectiveness'])
                    )
                    session['correct_mitigation'] = best_mitigation['id']
                
                # Log successo
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
                # Fase incorretta
                phase_info = CYBER_KILL_CHAIN_PHASES.get(correct_phase, {})
                
                # Log errore
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
        Valida la selezione della strategia di mitigazione
        
        Args:
            session_id (str): ID della sessione
            selected_mitigation (str): ID della mitigazione selezionata
            time_remaining (int): Tempo rimanente in secondi
            difficulty (str): Livello di difficoltà
            
        Returns:
            dict: Risultato della validazione con punti
        """
        try:
            # Valida input
            difficulty = validate_difficulty(difficulty)
            time_remaining = max(0, int(time_remaining))
            
            # Ottieni sessione
            session = GameService.get_or_create_session(session_id)
            correct_phase = session.get('correct_phase')
            
            if not correct_phase:
                raise ValueError("No active phase to validate mitigation")
            
            # Ottieni strategie per la fase corrente
            phase_mitigations = MITIGATION_STRATEGIES.get(correct_phase, [])
            selected_mit_data = next(
                (m for m in phase_mitigations if m['id'] == selected_mitigation), 
                None
            )
            
            if not selected_mit_data:
                raise ValueError(f"Invalid mitigation: {selected_mitigation}")
            
            # Valuta efficacia
            is_correct = selected_mit_data['effectiveness'] in ['High', 'Very High']
            
            # Calcola punti
            points = calculate_points(difficulty, time_remaining, True, is_correct)
            
            # Trova mitigazione ottimale
            best_mitigation = None
            correct_mitigation_id = session.get('correct_mitigation')
            if correct_mitigation_id:
                best_mitigation = next(
                    (m for m in phase_mitigations if m['id'] == correct_mitigation_id),
                    None
                )
            
            # Log risultato
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
        Ottiene le statistiche della sessione
        
        Args:
            session_id (str): ID della sessione
            
        Returns:
            dict: Statistiche della sessione
        """
        try:
            session = GameService.get_or_create_session(session_id)
            
            total_attempts = session.get('total_attempts', 0)
            correct_attempts = session.get('correct_attempts', 0)
            
            accuracy = 100.0
            if total_attempts > 0:
                accuracy = round((correct_attempts / total_attempts) * 100, 2)
            
            return {
                'total_games': total_attempts,
                'correct_answers': correct_attempts,
                'current_score': session.get('score', 0),
                'current_streak': session.get('streak', 0),
                'accuracy': accuracy,
                'session_created': session.get('created_at', '')
            }
            
        except Exception as e:
            logger.error(f"Error getting statistics for session {session_id}: {e}")
            raise
    
    @staticmethod
    def update_session_stats(session_id, points, is_correct):
        """
        Aggiorna le statistiche della sessione
        
        Args:
            session_id (str): ID della sessione
            points (int): Punti guadagnati
            is_correct (bool): Se la risposta era corretta
            
        Returns:
            dict: Statistiche aggiornate
        """
        try:
            session = GameService.get_or_create_session(session_id)
            
            # Aggiorna punti
            session['score'] = session.get('score', 0) + points
            
            # Aggiorna tentativi
            session['total_attempts'] = session.get('total_attempts', 0) + 1
            
            if is_correct:
                session['correct_attempts'] = session.get('correct_attempts', 0) + 1
                session['streak'] = session.get('streak', 0) + 1
            else:
                session['streak'] = 0
            
            # Log aggiornamento
            log_user_action(session_id, 'stats_updated', {
                'points_added': points,
                'is_correct': is_correct,
                'new_score': session['score'],
                'new_streak': session['streak']
            })
            
            return GameService.get_session_statistics(session_id)
            
        except Exception as e:
            logger.error(f"Error updating stats for session {session_id}: {e}")
            raise
    
    @staticmethod
    def get_global_leaderboard(limit=10):
        """
        Ottiene la classifica globale (mock data per demo)
        
        Args:
            limit (int): Numero massimo di risultati
            
        Returns:
            list: Lista dei migliori giocatori
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
            
            return mock_leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            raise
    
    @staticmethod
    def get_all_phases():
        """
        Ottiene tutte le fasi della Cyber Kill Chain
        
        Returns:
            list: Lista delle fasi con dettagli
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
        Resetta una sessione utente
        
        Args:
            session_id (str): ID della sessione da resettare
            
        Returns:
            bool: True se il reset è avvenuto con successo
        """
        try:
            if session_id in user_sessions:
                del user_sessions[session_id]
                log_user_action(session_id, 'session_reset', {})
                logger.info(f"Session {session_id} reset successfully")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error resetting session {session_id}: {e}")
            raise
    
    @staticmethod
    def get_session_count():
        """
        Ottiene il numero di sessioni attive
        
        Returns:
            int: Numero di sessioni attive
        """
        return len(user_sessions)
    
    @staticmethod
    def cleanup_old_sessions(max_age_hours=24):
        """
        Rimuove le sessioni vecchie per liberare memoria
        
        Args:
            max_age_hours (int): Età massima delle sessioni in ore
            
        Returns:
            int: Numero di sessioni rimosse
        """
        try:
            from datetime import datetime, timedelta
            
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            sessions_to_remove = []
            
            for session_id, session_data in user_sessions.items():
                created_at_str = session_data.get('created_at', '')
                if created_at_str:
                    try:
                        created_at = datetime.fromisoformat(created_at_str)
                        if created_at < cutoff_time:
                            sessions_to_remove.append(session_id)
                    except ValueError:
                        # Se non riesce a parsare la data, rimuovi la sessione
                        sessions_to_remove.append(session_id)
            
            # Rimuovi le sessioni vecchie
            for session_id in sessions_to_remove:
                del user_sessions[session_id]
                
            if sessions_to_remove:
                logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")
            
            return len(sessions_to_remove)
            
        except Exception as e:
            logger.error(f"Error cleaning up sessions: {e}")
            return 0