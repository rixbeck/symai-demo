"""
Configuration management utilities for SymbolicAI demos.
"""

from typing import Dict, Any

# Engine configuration definitions
ENGINE_CONFIGS = {
    'openai-comp': {
        'config_file': 'symai.config.openai.json',
        'display_name': 'OpenAI Compatible',
        'setup_message': 'OpenAI-compatible API',
    },
    'ollama': {
        'config_file': 'symai.config.ollama.json',
        'display_name': 'Ollama',
        'setup_message': 'Local Ollama LLM',
    }
}

def get_engine_config(engine_type: str) -> Dict[str, Any]:
    """Get configuration for a specific engine type."""
    return ENGINE_CONFIGS.get(engine_type)

def get_available_engines() -> Dict[str, Dict[str, Any]]:
    """Get all available engine configurations."""
    return ENGINE_CONFIGS

def is_valid_engine(engine_type: str) -> bool:
    """Check if the given engine type is valid."""
    return engine_type in ENGINE_CONFIGS