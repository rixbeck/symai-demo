#!/usr/bin/env python3
"""
Ollama Integration Test Script for SymbolicAI
=============================================

This script tests the Ollama integration with SymbolicAI to ensure
everything is working correctly with the local LLM setup.
"""

import json
import requests
from pathlib import Path

def test_ollama_server():
    """Test if Ollama server is running and accessible."""
    print("🔧 Testing Ollama Server Connection")
    print("=" * 50)
    
    try:
        # Try to connect to Ollama
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama server is running")
            
            if 'models' in models:
                print(f"📋 Available models:")
                for model in models['models']:
                    print(f"   • {model['name']} ({model.get('size', 'unknown size')})")
                return True
            else:
                print("⚠️  No models found")
                return False
        else:
            print(f"❌ Ollama server returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama server")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

def test_model_availability():
    """Test if the required model is available."""
    print("\n🤖 Testing Model Availability")
    print("=" * 50)
    
    # Load config to get the model name
    try:
        with open("symai.config.ollama.json") as f:
            config = json.load(f)
        
        model_name = config.get("NEUROSYMBOLIC_ENGINE_MODEL", "deepseek-r1:14b")
        print(f"Required model: {model_name}")
        
        # Check if model is available
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            available_models = [m['name'] for m in models.get('models', [])]
            
            if model_name in available_models:
                print(f"✅ Model {model_name} is available")
                return True
            else:
                print(f"❌ Model {model_name} not found")
                print(f"   Available models: {', '.join(available_models)}")
                print(f"   To install: ollama pull {model_name}")
                return False
        else:
            print("❌ Cannot check model availability")
            return False
            
    except FileNotFoundError:
        print("❌ Configuration file not found: symai.config.ollama.json")
        return False
    except Exception as e:
        print(f"❌ Error checking model: {e}")
        return False

def test_openai_compatibility():
    """Test Ollama's OpenAI-compatible API."""
    print("\n🔗 Testing OpenAI-Compatible API")
    print("=" * 50)
    
    try:
        # Load config
        with open("symai.config.ollama.json") as f:
            config = json.load(f)
        
        base_url = config.get("NEUROSYMBOLIC_ENGINE_BASE_URL", "http://localhost:11434/v1")
        model = config.get("NEUROSYMBOLIC_ENGINE_MODEL", "deepseek-r1:14b")
        
        # Test chat completions endpoint
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Say 'Hello, I am working correctly!' and nothing else."}
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer ollama"  # Ollama doesn't need real auth
        }
        
        print(f"Testing endpoint: {base_url}/chat/completions")
        print(f"Using model: {model}")
        
        response = requests.post(
            f"{base_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print(f"✅ API response: {content}")
                
                if "working correctly" in content.lower():
                    print("✅ Model is responding as expected")
                    return True
                else:
                    print("⚠️  Model responded but not as expected")
                    return True  # Still working, just different response
            else:
                print("❌ Invalid response format")
                return False
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_symbolicai_integration():
    """Test SymbolicAI integration with Ollama."""
    print("\n🧠 Testing SymbolicAI Integration")
    print("=" * 50)
    
    try:
        # Import and setup the engine
        from ollama_engine import setup_ollama_engine
        
        if not setup_ollama_engine():
            print("❌ Failed to setup Ollama engine")
            return False
        
        # Test basic SymbolicAI functionality
        from symai import Symbol
        
        print("Testing basic Symbol functionality...")
        test_symbol = Symbol("Hello from SymbolicAI!")
        
        # Test a simple query
        print("Sending query to local model...")
        response = test_symbol.query("Respond with: 'SymbolicAI integration working!'")
        
        print(f"Response: {response}")
        
        if "working" in str(response).lower():
            print("✅ SymbolicAI integration successful!")
            return True
        else:
            print("⚠️  Integration working but unexpected response")
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure SymbolicAI is installed")
        return False
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def test_configuration():
    """Test configuration file validity."""
    print("\n📁 Testing Configuration")
    print("=" * 50)
    
    config_file = Path("symai.config.ollama.json")
    
    if not config_file.exists():
        print("❌ Configuration file not found: symai.config.ollama.json")
        return False
    
    try:
        with open(config_file) as f:
            config = json.load(f)
        
        required_keys = [
            "NEUROSYMBOLIC_ENGINE_API_KEY",
            "NEUROSYMBOLIC_ENGINE_MODEL", 
            "NEUROSYMBOLIC_ENGINE_BASE_URL"
        ]
        
        for key in required_keys:
            if key in config:
                value = config[key]
                print(f"✅ {key}: {value}")
            else:
                print(f"❌ Missing required key: {key}")
                return False
        
        print("✅ Configuration file is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

def run_performance_test():
    """Run a simple performance test."""
    print("\n⚡ Performance Test")
    print("=" * 50)
    
    try:
        import time
        from ollama_engine import setup_ollama_engine
        from symai import Symbol
        
        if not setup_ollama_engine():
            print("❌ Cannot setup engine for performance test")
            return False
        
        # Simple performance test
        test_queries = [
            "What is 2+2?",
            "Name one color.",
            "Say hello."
        ]
        
        total_time = 0
        successful_queries = 0
        
        for i, query in enumerate(test_queries, 1):
            print(f"Query {i}: {query}")
            
            start_time = time.time()
            try:
                symbol = Symbol(query)
                response = symbol.query("Answer briefly.")
                end_time = time.time()
                
                query_time = end_time - start_time
                total_time += query_time
                successful_queries += 1
                
                print(f"   Response: {str(response)[:50]}...")
                print(f"   Time: {query_time:.2f}s")
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
        
        if successful_queries > 0:
            avg_time = total_time / successful_queries
            print(f"\n📊 Performance Summary:")
            print(f"   Successful queries: {successful_queries}/{len(test_queries)}")
            print(f"   Average response time: {avg_time:.2f}s")
            print(f"   Total time: {total_time:.2f}s")
            
            if avg_time < 5:
                print("✅ Good performance")
            elif avg_time < 15:
                print("⚠️  Moderate performance")
            else:
                print("🐌 Slow performance - consider using a smaller model")
            
            return True
        else:
            print("❌ No successful queries")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Ollama Integration Test Suite")
    print("================================")
    print("Testing SymbolicAI integration with local Ollama LLM")
    
    tests = [
        ("Ollama Server", test_ollama_server),
        ("Model Availability", test_model_availability),
        ("OpenAI Compatibility", test_openai_compatibility),
        ("Configuration", test_configuration),
        ("SymbolicAI Integration", test_symbolicai_integration),
        ("Performance", run_performance_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print(f"\n{'='*60}")
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ollama integration is working correctly.")
        print("\nYou can now run:")
        print("   ./symbolicai/bin/python main_ollama.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\nCommon solutions:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Pull the required model: ollama pull deepseek-r1:14b")
        print("3. Check the configuration file: symai.config.ollama.json")

if __name__ == "__main__":
    main()