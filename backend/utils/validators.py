"""
Input Validation Schemas
"""
from marshmallow import Schema, fields, validate, ValidationError, pre_load
from models.game_data import CYBER_KILL_CHAIN_PHASES, DIFFICULTY_CONFIG

class BaseSchema(Schema):
    """Schema base con utilities comuni"""
    
    @pre_load
    def strip_strings(self, data, **kwargs):
        """Rimuove spazi bianchi da stringhe"""
        if isinstance(data, dict):
            return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}
        return data

class SessionDataSchema(BaseSchema):
    """Validazione dati sessione"""
    session_id = fields.Str(
        required=True,
        validate=[
            validate.Length(min=5, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_-]+$', error="Invalid session ID format")
        ]
    )
    difficulty = fields.Str(
        missing='beginner',
        validate=validate.OneOf(list(DIFFICULTY_CONFIG.keys()))
    )
    stats = fields.Dict(missing=dict)

class PhaseValidationSchema(BaseSchema):
    """Validazione selezione fase"""
    session_id = fields.Str(
        required=True,
        validate=[
            validate.Length(min=5, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_-]+$')
        ]
    )
    selected_phase = fields.Str(
        required=True,
        validate=validate.OneOf(list(CYBER_KILL_CHAIN_PHASES.keys()))
    )

class MitigationValidationSchema(BaseSchema):
    """Validazione selezione mitigazione"""
    session_id = fields.Str(
        required=True,
        validate=[
            validate.Length(min=5, max=50),
            validate.Regexp(r'^[a-zA-Z0-9_-]+$')
        ]
    )
    selected_mitigation = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    time_remaining = fields.Int(
        missing=0,
        validate=validate.Range(min=0, max=300)  # Max 5 minuti
    )
    difficulty = fields.Str(
        missing='beginner',
        validate=validate.OneOf(list(DIFFICULTY_CONFIG.keys()))
    )

class StatsSchema(BaseSchema):
    """Validazione statistiche giocatore"""
    score = fields.Int(validate=validate.Range(min=0, max=999999), missing=0)
    streak = fields.Int(validate=validate.Range(min=0, max=1000), missing=0)
    accuracy = fields.Float(validate=validate.Range(min=0, max=100), missing=100)

def validate_json_input(schema_class):
    """
    Decorator per validare input JSON con schema Marshmallow
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            from flask import request, jsonify
            from utils.helpers import format_api_response
            
            try:
                # Controlla se è JSON
                if not request.is_json:
                    return jsonify(format_api_response(
                        False, error="Content-Type must be application/json"
                    )), 400
                
                data = request.get_json()
                if not data:
                    return jsonify(format_api_response(
                        False, error="No JSON data provided"
                    )), 400
                
                # Valida con schema
                schema = schema_class()
                validated_data = schema.load(data)
                
                # Passa i dati validati alla funzione
                return f(validated_data, *args, **kwargs)
                
            except ValidationError as e:
                return jsonify(format_api_response(
                    False, 
                    error=f"Validation error: {e.messages}"
                )), 400
            except Exception as e:
                return jsonify(format_api_response(
                    False, error=f"Invalid request: {str(e)}"
                )), 400
        
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator