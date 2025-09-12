"""
Rate Limiting Configuration
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import os
import logging

logger = logging.getLogger(__name__)

def create_limiter(app):
    """
    Crea e configura il rate limiter
    """
    try:
        # Prova a connettersi a Redis (produzione)
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        redis_client = redis.from_url(redis_url)
        redis_client.ping()  # Test connessione
        
        storage_uri = redis_url
        logger.info("Rate limiter using Redis storage")
        
    except (redis.ConnectionError, redis.TimeoutError):
        # Fallback a memoria (sviluppo)
        storage_uri = "memory://"
        logger.warning("Rate limiter using memory storage (development only)")
    
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=storage_uri,
        default_limits=["1000 per hour", "100 per minute"],
        headers_enabled=True,  # Mostra limiti negli headers
        strategy="fixed-window"
    )
    
    return limiter

def get_user_key():
    """
    Genera chiave per rate limiting basata su IP + session_id
    """
    from flask import request
    
    ip = get_remote_address()
    session_id = request.json.get('session_id', '') if request.json else ''
    
    return f"{ip}:{session_id[:10]}"  # IP + primi 10 char di session_id