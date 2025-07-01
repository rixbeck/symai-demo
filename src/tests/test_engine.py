#!/usr/bin/env python3
"""
Unified Engine Test Script for SymbolicAI
=======================================

Tests engine integrations (OpenAI-compatible, Ollama, etc.) with command-line selection.
Usage: python -m src.tests.test_engine [openai-comp|ollama]
"""

import json
import sys
import time
import requests
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

from symai import Symbol
from symai.functional import EngineRepository
from ..engines.engine_manager import EngineManager
from ..utils.config import ENGINE_CONFIGS, is_valid_engine, get_engine_config

def is_local_endpoint(url: str) -> bool:
    """Check if the endpoint is local."""
    return "localhost" in url or "127.0.0.1" in url

def load_config(engine_type: str) -> Dict[str, Any]:
    """Load engine configuration."""
    config_file = ENGINE_CONFIGS[engine_type]['config_file']
    
    # Define default values for each engine type
    defaults = {
        'openai-comp': {
            'default_base_url': 'https://api.openai.com/v1',
            'default_model': 'gpt-4'
        },
        'ollama': {
            'default_base_url': 'http://localhost:11434/v1',
            'default_model': 'deepseek-r1:14b'
        }
    }
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        # Set defaults if not specified
        engine_defaults = defaults.get(engine_type, {})
        config.setdefault('NEUROSYMBOLIC_ENGINE_BASE_URL',
                         engine_defaults.get('default_base_url'))
        config.setdefault('NEUROSYMBOLIC_ENGINE_MODEL',
                         engine_defaults.get('default_model'))
        
        return config
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        sys.exit(1)

def verify_config(config: Dict[str, Any], engine_type: str) -> bool:
    """Verify the configuration values."""
    base_url = config.get("NEUROSYMBOLIC_ENGINE_BASE_URL")
    model = config.get("NEUROSYMBOLIC_ENGINE_MODEL")
    api_key = config.get("NEUROSYMBOLIC_ENGINE_API_KEY")
    
    if not base_url or not model:
        print("❌ Missing required configuration values")
        return False
        
    if engine_type == 'openai-comp' and not is_local_endpoint(base_url):
        if not api_key or api_key == "<YOUR_OPENAI_API_KEY>" or len(api_key) < 20:
            print("❌ Invalid OpenAI API key")
            return False
            
    return True

def test_basic_query(engine_type: str) -> bool:
    """Test basic query functionality."""
    print("\n✨ Testing Basic Query")
    print("=" * 50)
    
    try:
        # Create test symbol
        symbol = Symbol("Test engine integration")
        response = symbol.query("Say 'Integration test successful!' and nothing else.")
        print(f"Response: {response}")
        
        if "successful" in str(response).lower():
            print("✅ Basic query test passed!")
            return True
        else:
            print("❌ Basic query test failed - unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ Basic query test failed: {e}")
        return False

def test_context_handling() -> bool:
    """Test context handling capabilities."""
    print("\n✨ Testing Context Handling")
    print("=" * 50)
    
    try:
        # Test with specific context
        data = "The sky is blue"
        context = "Respond in exactly 5 words"
        symbol = Symbol(data)
        
        print(f"Data: '{data}'")
        print(f"Context: '{context}'")
        response = symbol.query(context=context)
        print(f"Response: {response}")
        
        words = str(response).split()
        if len(words) == 5:
            print("✅ Context test passed!")
            return True
        else:
            print(f"❌ Context test failed - expected 5 words, got {len(words)}")
            return False
            
    except Exception as e:
        print(f"❌ Context test failed: {e}")
        return False

def test_model_performance() -> bool:
    """Test model performance with multiple queries."""
    print("\n⚡ Testing Performance")
    print("=" * 50)
    
    test_queries = [
        "What is 2+2?",
        "Name a color.",
        "Say hello."
    ]
    
    total_time = 0
    successful = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: {query}")
        start_time = time.time()
        
        try:
            symbol = Symbol(query)
            response = symbol.query("Answer briefly.")
            query_time = time.time() - start_time
            
            print(f"Response: {str(response)[:50]}...")
            print(f"Time: {query_time:.2f}s")
            
            total_time += query_time
            successful += 1
            
        except Exception as e:
            print(f"❌ Query failed: {e}")
    
    if successful > 0:
        avg_time = total_time / successful
        print(f"\n📊 Performance Summary:")
        print(f"Successful queries: {successful}/{len(test_queries)}")
        print(f"Average response time: {avg_time:.2f}s")
        return True
    return False

def run_tests(engine_type: str) -> Tuple[int, int]:
    """Run all tests for the specified engine."""
    tests = [
        ("Basic Query", test_basic_query, engine_type),
        ("Context Handling", test_context_handling),
        ("Performance", test_model_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_info in tests:
        test_name = test_info[0]
        test_func = test_info[1]
        test_args = test_info[2:]
        
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        
        try:
            if test_func(*test_args):
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            
    return passed, total

def main():
    """Main test execution function."""
    if len(sys.argv) != 2 or not is_valid_engine(sys.argv[1]):
        print("Usage: python -m src.tests.test_engine [openai-comp|ollama]")
        print("\nAvailable engines:")
        for engine in ENGINE_CONFIGS:
            print(f"  • {engine}")
        sys.exit(1)
    
    engine_type = sys.argv[1]
    config_file = ENGINE_CONFIGS[engine_type]['config_file']
    
    print(f"🔬 Testing {engine_type.upper()} Engine Integration")
    print("=" * 50)
    print(f"Using config: {config_file}")
    
    try:
        # Load and verify configuration
        config = load_config(engine_type)
        if not verify_config(config, engine_type):
            sys.exit(1)
        
        # Get configuration values
        base_url = config.get('NEUROSYMBOLIC_ENGINE_BASE_URL')
        api_key = config.get('NEUROSYMBOLIC_ENGINE_API_KEY')
        model = config.get('NEUROSYMBOLIC_ENGINE_MODEL')
        
        print(f"\nConfiguration:")
        print(f"  Base URL: {base_url}")
        print(f"  Model: {model}")
        print(f"  API Key: {'<configured>' if api_key else '<missing>'}")
        
        # Test connection
        print("\nTesting connection...")
        if not EngineManager.test_engine_connection(engine_type, base_url=base_url, api_key=api_key):
            print(f"❌ Cannot connect to {engine_type} engine")
            print("   Please check your configuration and API key")
            sys.exit(1)
            
        # Setup engine
        print("\nSetting up engine...")
        if not EngineManager.setup_engine(engine_type, config_path=config_file):
            print(f"❌ Failed to setup {engine_type} engine")
            sys.exit(1)
            
        # Run tests
        print("\nRunning integration tests...")
        passed, total = run_tests(engine_type)
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"🎯 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print(f"🎉 All {engine_type} integration tests passed!")
        else:
            print(f"⚠️  Some tests failed. Check the errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()