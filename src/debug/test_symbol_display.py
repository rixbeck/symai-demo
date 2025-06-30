#!/usr/bin/env python3
"""
Test to debug Symbol display issues
Usage: python -m src.debug.test_symbol_display
"""

from symai import Symbol
from ..engines.engine_manager import EngineManager

def test_symbol_content():
    """Test how Symbol objects handle content"""
    print("🔍 Testing Symbol Content Handling")
    print("=" * 50)
    
    try:
        # Setup engine
        if not EngineManager.setup_engine('ollama', allow_override=True):
            print("❌ Failed to setup Ollama engine")
            return
        
        # Test 1: Simple query
        print("\n1. Simple Query Test:")
        symbol = Symbol("Test")
        result = symbol.query("Say 'Hello World' and explain why this is a greeting.")
        
        print(f"Result type: {type(result)}")
        print(f"Result repr: {repr(result)}")
        print(f"Result str: {str(result)}")
        
        # Check if result has a value attribute
        if hasattr(result, 'value'):
            print(f"Result.value: {repr(result.value)}")
            print(f"Result.value type: {type(result.value)}")
        
        # Check if result has content attribute
        if hasattr(result, 'content'):
            print(f"Result.content: {repr(result.content)}")
        
        # Test 2: Direct engine test
        print("\n2. Direct Engine Test:")
        from ..engines.ollama_engine import OllamaEngine
        
        engine = OllamaEngine()
        
        class MockArg:
            def __init__(self):
                self.prop = MockProp()
                self.kwargs = {}
        
        class MockProp:
            def __init__(self):
                self.preprocessed_input = "Say 'Direct engine test successful' and nothing else."
        
        arg = MockArg()
        engine.prepare(arg)
        content, metadata = engine.forward(arg)
        
        print(f"Direct engine response: {repr(content)}")
        print(f"Direct engine content: {content}")
        print(f"Metadata: {metadata}")
        
        # Test 3: Symbol creation and access
        print("\n3. Symbol Creation Test:")
        test_symbol = Symbol("Testing symbol creation")
        print(f"Symbol: {test_symbol}")
        print(f"Symbol type: {type(test_symbol)}")
        print(f"Symbol repr: {repr(test_symbol)}")
        
        # Test 4: Try different query types
        print("\n4. Different Query Types:")
        
        # Short response
        short_result = test_symbol.query("Say 'OK'")
        print(f"Short result: {repr(short_result)}")
        print(f"Short result str: {str(short_result)}")
        
        # Math response
        math_result = test_symbol.query("What is 2+2? Answer with just the number.")
        print(f"Math result: {repr(math_result)}")
        print(f"Math result str: {str(math_result)}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run symbol content tests."""
    test_symbol_content()

if __name__ == "__main__":
    main()