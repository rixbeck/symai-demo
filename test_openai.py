#!/usr/bin/env python3
"""
Test script for OpenAI engine integration with SymbolicAI
=======================================================

This script tests the OpenAI engine implementation with either
OpenAI's API or a local/custom OpenAI-compatible endpoint.
"""

import json
import sys
from symai import Symbol
from openai_engine import OpenAIEngine, setup_openai_engine, test_openai_connection


def is_local_endpoint(url: str) -> bool:
    """Check if the endpoint is local."""
    return "localhost" in url or "127.0.0.1" in url


def load_config(config_path: str = "symai.config.openai.json"):
    """Load the OpenAI configuration."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        sys.exit(1)


def run_basic_test(base_url: str, model: str, api_key: str):
    """Run a basic test query using the OpenAI engine."""
    try:
        # Create engine instance
        engine = OpenAIEngine(base_url=base_url, model=model, api_key=api_key)
        engine.verbose = True
        print("\n✨ Testing simple query...")
        
        # Create test symbol
        symbol = Symbol("Test OpenAI integration")
        
        # Test basic query
        print("\n🧪 Query: 'Respond with exactly: OpenAI test successful!'")
        response = symbol.query("Respond with exactly: OpenAI test successful!")
        print(f"🎯 Response: {response}")
        
        # Verify response
        if "OpenAI test successful" in str(response):
            print("✅ Basic query test passed!")
        else:
            print("❌ Basic query test failed - unexpected response")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


def run_context_test(base_url: str, model: str, api_key: str):
    """Test handling of context and complex queries."""
    try:
        # Create engine instance
        engine = OpenAIEngine(base_url=base_url, model=model, api_key=api_key)
        engine.verbose = True
        print("\n✨ Testing context handling...")
        
        # Create test symbol with context
        data = "The sky is blue"
        context = "Respond in exactly 5 words"
        symbol = Symbol(data)
        
        # Test query with context
        print(f"\n🧪 Data: '{data}'")
        print(f"Context: '{context}'")
        response = symbol.query(context=context)
        print(f"🎯 Response: {response}")
        
        # Verify response length
        words = str(response).split()
        if len(words) == 5:
            print("✅ Context test passed!")
        else:
            print(f"❌ Context test failed - expected 5 words, got {len(words)}")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


def verify_config(config: dict) -> bool:
    """Verify the configuration values."""
    base_url = config.get("NEUROSYMBOLIC_ENGINE_BASE_URL")
    model = config.get("NEUROSYMBOLIC_ENGINE_MODEL")
    api_key = config.get("NEUROSYMBOLIC_ENGINE_API_KEY")
    
    if not base_url:
        print("❌ NEUROSYMBOLIC_ENGINE_BASE_URL is missing")
        return False
        
    if not model:
        print("❌ NEUROSYMBOLIC_ENGINE_MODEL is missing")
        return False
        
    if not api_key:
        print("❌ NEUROSYMBOLIC_ENGINE_API_KEY is missing")
        return False
        
    # For OpenAI API endpoints, verify API key format
    if not is_local_endpoint(base_url) and (api_key == "<YOUR_OPENAI_API_KEY>" or len(api_key) < 20):
        print("❌ Please add your OpenAI API key to symai.config.openai.json")
        return False
        
    return True


def main():
    """Main test execution function."""
    print("🔬 OpenAI/Compatible Engine Integration Tests")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    # Verify config
    if not verify_config(config):
        sys.exit(1)
    
    base_url = config["NEUROSYMBOLIC_ENGINE_BASE_URL"]
    model = config["NEUROSYMBOLIC_ENGINE_MODEL"]
    api_key = config["NEUROSYMBOLIC_ENGINE_API_KEY"]
    
    # Detect if using local endpoint
    if is_local_endpoint(base_url):
        print(f"📍 Using local OpenAI-compatible endpoint: {base_url}")
    else:
        print(f"🌐 Using OpenAI API endpoint: {base_url}")
    
    # Test API connection
    if test_openai_connection(base_url=base_url, api_key=api_key):
        # Setup engine
        if setup_openai_engine("symai.config.openai.json"):
            print("\n🚀 Running integration tests...")
            
            # Run tests
            run_basic_test(base_url, model, api_key)
            run_context_test(base_url, model, api_key)
            
            print("\n🎉 All tests completed!")
        else:
            print("\n❌ Failed to setup engine")
    else:
        if is_local_endpoint(base_url):
            print("\n❌ Local OpenAI-compatible endpoint not accessible")
            print(f"\nMake sure your local server is running at {base_url}")
        else:
            print("\n❌ OpenAI API not accessible")
            print("\nTo use OpenAI API:")
            print("1. Get an API key from https://platform.openai.com/")
            print("2. Add it to symai.config.openai.json")
            print("3. Make sure you have an active subscription")


if __name__ == "__main__":
    main()