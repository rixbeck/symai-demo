#!/usr/bin/env python3
"""
SymbolicAI Playground - Unified Demonstration
==========================================

This is the main demonstration script for SymbolicAI, supporting both OpenAI and Ollama
backends through a unified interface. Each demo adapts its functionality based on the
selected engine, ensuring compatibility across both cloud and local LLM implementations.

Supported Engines:
- OpenAI: Cloud-based API access to GPT models
- Ollama: Local LLM integration with various models

Usage:
    python main.py [openai|ollama]

Examples:
    python main.py openai    # Run demos using OpenAI's cloud API
    python main.py ollama    # Run demos using local Ollama installation

Notes:
- Each demo adapts to the selected engine's capabilities
- Semantic operations are consistently available across both engines
- Configuration files:
  * OpenAI: symai.config.openai.json
  * Ollama: symai.config.ollama.json
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Import modules from the new structure
from src.engines.engine_manager import EngineManager
from src.demos import demos
from src.utils.config import ENGINE_CONFIGS, is_valid_engine, get_engine_config

# Global engine state
current_engine: Dict[str, Any] = {'type': None, 'config': None}

def check_setup(engine_type: str):
    """Check if the setup is correct before proceeding."""
    if not is_valid_engine(engine_type):
        print(f"❌ Unknown engine type: {engine_type}")
        print("Available engines:", ", ".join(ENGINE_CONFIGS.keys()))
        return False

    config = get_engine_config(engine_type)
    print(f"🔧 Checking SymbolicAI setup for {config['display_name']}...")
    print(f"Using {config['setup_message']}")
    
    if EngineManager.setup_engine(engine_type, config_path=config['config_file']):
        print(f"✅ {config['display_name']} configuration and setup successful!")
        return True
        
    print(f"❌ {config['display_name']} setup failed - please check your configuration.")
    return False

def main():
    """Main demonstration function."""
    global current_engine

    # Parse command-line argument
    if len(sys.argv) != 2 or not is_valid_engine(sys.argv[1]):
        print("Usage: python main.py [openai|ollama]")
        print("\nAvailable engines:")
        for engine, config in ENGINE_CONFIGS.items():
            print(f"  • {engine:<10} - {config['setup_message']}")
        return

    # Set global engine state
    current_engine['type'] = sys.argv[1]
    current_engine['config'] = get_engine_config(current_engine['type'])
    
    # Share current_engine state with demos module
    demos.current_engine = current_engine
    
    print(f"🎭 SymbolicAI Playground - {current_engine['config']['display_name']} Demo")
    print("=" * (24 + len(current_engine['config']['display_name'])))
    print(f"A comprehensive demonstration using {current_engine['config']['setup_message']}")
    
    # Check setup first
    if not check_setup(current_engine['type']):
        print(f"\n❌ {current_engine['config']['display_name']} setup incomplete.")
        print(f"   Please check {current_engine['config']['config_file']}")
        return
    
    try:
        # Run all demonstrations
        demos.demo_basic_symbols()
        demos.demo_symbol_operations()
        demos.demo_data_processing()
        demos.demo_contracts_basic()
        demos.demo_configuration()
        demos.demo_embeddings()
        demos.demo_advanced_features()
        
        print("\n" + "="*60)
        engine_name = current_engine['config']['display_name']
        print(f"🎉 {engine_name} Demo completed successfully!")
        print("="*60)
        print("\n🔗 Next steps:")
        
        # Engine-specific resources
        if current_engine['type'] == 'openai':
            print("1. Explore OpenAI models: https://platform.openai.com/docs/models")
            print("2. OpenAI API documentation: https://platform.openai.com/docs/api-reference")
        else:
            print("1. Explore Ollama models: https://ollama.ai/library")
            print("2. Ollama documentation: https://github.com/ollama/ollama")
        
        # Common resources
        print("3. SymbolicAI documentation: https://extensityai.gitbook.io/symbolicai")
        print("4. Example applications: https://github.com/ExtensityAI/symbolicai/tree/main/examples")
        print(f"5. Build your own {engine_name}-powered neuro-symbolic applications!")
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure SymbolicAI is properly installed.")
        print("Run: ./symbolicai/bin/pip install symbolicai")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Check your configuration and try again.")

if __name__ == "__main__":
    main()