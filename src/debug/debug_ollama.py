#!/usr/bin/env python3
"""
Debug script to investigate Ollama integration issues
Usage: python -m src.debug.debug_ollama
"""

import json
import requests
from symai import Symbol
from ..engines.engine_manager import EngineManager

def test_direct_ollama_api():
    """Test Ollama API directly"""
    print("🔍 Testing Ollama API directly")
    print("=" * 50)
    
    # Test using the native Ollama API
    payload = {
        "model": "deepseek-r1:14b",
        "prompt": "Say 'Hello from Ollama!' and nothing else.",
        "stream": False
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            result = response.json()
            content = result.get("response", "")
            print(f"Native API response: {repr(content)}")
            print(f"Visible content: {content}")
        else:
            print(f"API failed: {response.status_code}")
    except requests.RequestException as e:
        print(f"Connection failed: {e}")

def test_openai_compatible_api():
    """Test OpenAI-compatible API"""
    print("\n🔍 Testing OpenAI-compatible API")
    print("=" * 50)
    
    payload = {
        "model": "deepseek-r1:14b",
        "messages": [{"role": "user", "content": "Say 'Hello from OpenAI API!' and nothing else."}],
        "max_tokens": 100
    }
    
    try:
        response = requests.post("http://localhost:11434/v1/chat/completions", json=payload)
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                print(f"OpenAI API response: {repr(content)}")
                print(f"Visible content: {content}")
        else:
            print(f"API failed: {response.status_code}")
    except requests.RequestException as e:
        print(f"Connection failed: {e}")

def test_engine_direct():
    """Test our engine directly"""
    print("\n🔍 Testing our OllamaEngine directly")
    print("=" * 50)
    
    try:
        from ..engines.ollama_engine import OllamaEngine
        
        engine = OllamaEngine()
        
        # Create a mock argument object
        class MockArgument:
            def __init__(self):
                self.prop = MockProp()
                self.kwargs = {}
        
        class MockProp:
            def __init__(self):
                self.preprocessed_input = "Say 'Hello from Engine!' and nothing else."
        
        arg = MockArgument()
        engine.prepare(arg)
        
        result, metadata = engine.forward(arg)
        print(f"Engine response: {repr(result)}")
        print(f"Visible content: {result}")
        print(f"Metadata: {metadata}")
    except ImportError as e:
        print(f"Failed to import OllamaEngine: {e}")
    except Exception as e:
        print(f"Engine test failed: {e}")

def test_symbolicai_integration():
    """Test SymbolicAI integration"""
    print("\n🔍 Testing SymbolicAI integration")
    print("=" * 50)
    
    try:
        # Setup engine
        if EngineManager.setup_engine('ollama', allow_override=True):
            print("✅ Engine setup successful")
            
            # Test simple query
            symbol = Symbol("Test")
            result = symbol.query("Say 'Hello from SymbolicAI!' and nothing else.")
            
            print(f"SymbolicAI response: {repr(result)}")
            print(f"Visible content: {result}")
            print(f"Type: {type(result)}")
        else:
            print("❌ Engine setup failed")
    except Exception as e:
        print(f"SymbolicAI integration test failed: {e}")

def test_semantic_operations():
    """Test semantic operations specifically"""
    print("\n🔍 Testing semantic operations")
    print("=" * 50)
    
    try:
        if EngineManager.setup_engine('ollama', allow_override=True):
            text = Symbol("Cats are adorable pets")
            print(f"Original: {text}")
            
            # Test semantic contains - this should work
            try:
                result = 'feline' in text.sem
                print(f"'feline' in text.sem: {result}")
                
                # Let's see what the actual query is
                from symai.symbol import Symbol as SymbolClass
                print(f"Symbol type: {type(text)}")
                
            except Exception as e:
                print(f"Semantic operation failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ Engine setup failed")
    except Exception as e:
        print(f"Semantic operations test failed: {e}")

def main():
    """Run all debug tests."""
    print("🐛 Debugging Ollama Integration Issues")
    print("=" * 60)
    
    debug_tests = [
        test_direct_ollama_api,
        test_openai_compatible_api,
        test_engine_direct,
        test_symbolicai_integration,
        test_semantic_operations
    ]
    
    for test in debug_tests:
        try:
            test()
            print("\n" + "-" * 60)
        except Exception as e:
            print(f"❌ Debug test {test.__name__} failed: {e}")
            print("-" * 60)

if __name__ == "__main__":
    main()