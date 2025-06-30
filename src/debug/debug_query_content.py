#!/usr/bin/env python3
"""
Debug script to check what content is actually being sent to Ollama
Usage: python -m src.debug.debug_query_content
"""

from symai import Symbol
from symai.functional import EngineRepository
from ..engines.engine_manager import EngineManager

def debug_query_content():
    """Debug what content is being sent to the model"""
    print("🔍 Debugging Query Content")
    print("=" * 50)
    
    try:
        from ..engines.ollama_engine import OllamaEngine
        
        # Create a custom debug engine that logs everything
        class DebugOllamaEngine(OllamaEngine):
            def prepare(self, argument):
                print(f"\n📥 PREPARE METHOD DEBUG:")
                print(f"  argument type: {type(argument)}")
                print(f"  argument.prop: {argument.prop}")
                print(f"  argument.prop.preprocessed_input: {repr(argument.prop.preprocessed_input)}")
                print(f"  argument.kwargs: {argument.kwargs}")
                print(f"  argument.args: {argument.args}")
                
                # Call parent prepare method
                super().prepare(argument)
                
                print(f"  prepared_input: {argument.prop.prepared_input}")
                
            def forward(self, argument):
                print(f"\n📤 FORWARD METHOD DEBUG:")
                payload = argument.prop.prepared_input
                print(f"  payload being sent: {payload}")
                
                # Call parent forward method
                result = super().forward(argument)
                print(f"  result: {result}")
                return result
        
        # Register debug engine
        debug_engine = DebugOllamaEngine()
        debug_engine.verbose = True
        EngineRepository.register('neurosymbolic', debug_engine, allow_engine_override=True)
        
        print("\n1. Testing direct Symbol query:")
        print("-" * 30)
        symbol = Symbol("Test input")
        print(f"Symbol content: {symbol}")
        print(f"Symbol value: {symbol.value if hasattr(symbol, 'value') else 'N/A'}")
        
        result = symbol.query("Say 'Hello World' exactly")
        print(f"Query result: {result}")
        
        print("\n2. Testing composition:")
        print("-" * 30)
        idea = Symbol("artificial intelligence")
        print(f"Idea content: {idea}")
        comp_result = idea.compose()
        print(f"Composition result: {comp_result}")
        
        print("\n3. Testing translation:")
        print("-" * 30)
        hello = Symbol("Hello, how are you?")
        print(f"Hello content: {hello}")
        trans_result = hello.query("Translate this to German")
        print(f"Translation result: {trans_result}")
        
    except ImportError as e:
        print(f"❌ Failed to import OllamaEngine: {e}")
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run debug query content analysis."""
    debug_query_content()

if __name__ == "__main__":
    main()