#!/usr/bin/env python3
"""
Debug script to investigate Ollama integration issues
"""

import json
import requests
from ollama_engine import setup_ollama_engine
from symai import Symbol

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
    
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    if response.status_code == 200:
        result = response.json()
        content = result.get("response", "")
        print(f"Native API response: {repr(content)}")
        print(f"Visible content: {content}")
    else:
        print(f"API failed: {response.status_code}")

def test_openai_compatible_api():
    """Test OpenAI-compatible API"""
    print("\n🔍 Testing OpenAI-compatible API")
    print("=" * 50)
    
    payload = {
        "model": "deepseek-r1:14b",
        "messages": [{"role": "user", "content": "Say 'Hello from OpenAI API!' and nothing else."}],
        "max_tokens": 100
    }
    
    response = requests.post("http://localhost:11434/v1/chat/completions", json=payload)
    if response.status_code == 200:
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"]
            print(f"OpenAI API response: {repr(content)}")
            print(f"Visible content: {content}")
    else:
        print(f"API failed: {response.status_code}")

def test_engine_direct():
    """Test our engine directly"""
    print("\n🔍 Testing our OllamaEngine directly")
    print("=" * 50)
    
    from ollama_engine import OllamaEngine
    
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

def test_symbolicai_integration():
    """Test SymbolicAI integration"""
    print("\n🔍 Testing SymbolicAI integration")
    print("=" * 50)
    
    # Setup engine
    setup_ollama_engine(allow_override=True)
    
    # Test simple query
    symbol = Symbol("Test")
    result = symbol.query("Say 'Hello from SymbolicAI!' and nothing else.")
    
    print(f"SymbolicAI response: {repr(result)}")
    print(f"Visible content: {result}")
    print(f"Type: {type(result)}")

def test_semantic_operations():
    """Test semantic operations specifically"""
    print("\n🔍 Testing semantic operations")
    print("=" * 50)
    
    setup_ollama_engine(allow_override=True)
    
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

if __name__ == "__main__":
    print("🐛 Debugging Ollama Integration Issues")
    print("=" * 60)
    
    test_direct_ollama_api()
    test_openai_compatible_api() 
    test_engine_direct()
    test_symbolicai_integration()
    test_semantic_operations()