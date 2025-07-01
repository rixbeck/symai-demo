#!/usr/bin/env python3
"""
SymbolicAI Engine Manager
========================

This module provides centralized engine management for SymbolicAI,
allowing dynamic engine setup based on configuration.
"""

import json
from typing import Optional
from symai.functional import EngineRepository
from .openai_engine import OpenAIEngine, test_openai_connection
from .ollama_engine import OllamaEngine, test_ollama_connection

class EngineManager:
    """
    Centralized engine management for SymbolicAI.
    Handles setup and configuration of different engine types.
    """
    
    ENGINE_TYPES = {
        'openai-comp': {
            'class': OpenAIEngine,
            'test_func': test_openai_connection,
            'default_config': 'symai.config.openai.json',
            'default_base_url': 'https://api.openai.com/v1',
            'default_model': 'gpt-4'
        },
        'ollama': {
            'class': OllamaEngine,
            'test_func': test_ollama_connection,
            'default_config': 'symai.config.ollama.json',
            'default_base_url': 'http://localhost:11434/v1',
            'default_model': 'deepseek-r1:14b'
        }
    }

    @staticmethod
    def setup_engine(engine_type: str, config_path: Optional[str] = None, allow_override: bool = True) -> bool:
        """
        Set up and register an engine with SymbolicAI.

        Args:
            engine_type: Type of engine to setup ('openai-comp' or 'ollama')
            config_path: Path to the configuration file. If None, uses default for engine type.
            allow_override: Whether to allow overriding existing engine

        Returns:
            bool: True if setup was successful, False otherwise
        """
        try:
            # Validate engine type
            if engine_type not in EngineManager.ENGINE_TYPES:
                print(f"❌ Unknown engine type: {engine_type}")
                print(f"   Available types: {list(EngineManager.ENGINE_TYPES.keys())}")
                return False

            # Get engine configuration
            engine_config = EngineManager.ENGINE_TYPES[engine_type]
            config_file = config_path or engine_config['default_config']

            # Load configuration
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except FileNotFoundError:
                print(f"❌ Configuration file not found: {config_file}")
                return False
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON in configuration file: {e}")
                return False

            # Extract configuration values
            base_url = config.get("NEUROSYMBOLIC_ENGINE_BASE_URL", engine_config['default_base_url'])
            model = config.get("NEUROSYMBOLIC_ENGINE_MODEL", engine_config['default_model'])
            api_key = config.get("NEUROSYMBOLIC_ENGINE_API_KEY")

            # Validate API key for OpenAI
            if engine_type == 'openai-comp' and (not api_key or api_key == "<YOUR_OPENAI_API_KEY>"):
                print("❌ OpenAI API key not found in config")
                return False

            # Test connection if applicable
            test_func = engine_config.get('test_func')
            if test_func:
                if engine_type == 'openai-comp':
                    if not test_func(base_url, api_key):
                        return False
                else:
                    if not test_func(base_url):
                        return False

            # Create engine instance
            engine_class = engine_config['class']
            engine = engine_class(base_url=base_url, model=model, api_key=api_key)

            # Register engine
            if allow_override or 'neurosymbolic' not in EngineRepository._engines:
                EngineRepository.register('neurosymbolic', engine, allow_engine_override=allow_override)
                print(f"✅ {engine_type.title()} engine registered successfully!")
                print(f"   Base URL: {base_url}")
                print(f"   Model: {model}")
                return True
            else:
                print("⚠️  Engine already registered. Use allow_override=True to replace.")
                return False

        except Exception as e:
            print(f"❌ Failed to setup {engine_type} engine: {e}")
            return False

    @staticmethod
    def test_engine_connection(engine_type: str, base_url: Optional[str] = None, api_key: Optional[str] = None) -> bool:
        """
        Test connection to a specific engine.

        Args:
            engine_type: Type of engine to test ('openai-comp' or 'ollama')
            base_url: Base URL for the API (optional)
            api_key: API key for authentication (optional, required for OpenAI)

        Returns:
            bool: True if connection successful, False otherwise
        """
        if engine_type not in EngineManager.ENGINE_TYPES:
            print(f"❌ Unknown engine type: {engine_type}")
            return False

        engine_config = EngineManager.ENGINE_TYPES[engine_type]
        test_func = engine_config['test_func']
        
        if not base_url:
            base_url = engine_config['default_base_url']

        try:
            if engine_type == 'openai-comp':
                return test_func(base_url, api_key)
            else:
                return test_func(base_url)
        except Exception as e:
            print(f"❌ Failed to test {engine_type} connection: {e}")
            return False


if __name__ == "__main__":
    # Test both engine setups
    print("🔧 Testing Engine Setup")
    print("="*50)

    # Test OpenAI setup
    print("\nTesting OpenAI setup...")
    if EngineManager.setup_engine('openai-comp'):
        print("OpenAI-compatible setup successful!")
    else:
        print("OpenAI setup failed!")

    # Test Ollama setup
    print("\nTesting Ollama setup...")
    if EngineManager.setup_engine('ollama'):
        print("Ollama setup successful!")
    else:
        print("Ollama setup failed!")