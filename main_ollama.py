#!/usr/bin/env python3
"""
SymbolicAI with Ollama - Local LLM Demonstration
===============================================

This script demonstrates how to use SymbolicAI with a local Ollama provider
using OpenAI-compatible API. This allows you to run neuro-symbolic AI
applications completely locally without requiring cloud API keys.

Prerequisites:
1. Install Ollama: https://ollama.ai/
2. Pull a model: ollama pull deepseek-r1:14b
3. Start Ollama server: ollama serve
"""

import os
import sys
import json
from pathlib import Path

def check_ollama_setup():
    """Check if Ollama is properly configured and running."""
    print("🔧 Checking Ollama Setup...")
    print("=" * 60)
    
    # Import the engine manager
    try:
        from engine_manager import EngineManager
    except ImportError as e:
        print(f"❌ Cannot import engine_manager: {e}")
        return False
    
    # Setup the engine using EngineManager
    if not EngineManager.setup_engine('ollama', config_path="symai.config.ollama.json"):
        print("❌ Failed to setup Ollama engine")
        return False
    
    print("✅ Ollama setup complete!")
    return True

def demo_basic_symbols_ollama():
    """Demonstrate basic Symbol usage with Ollama."""
    print("\n" + "="*60)
    print("📝 DEMO 1: Basic Symbol Usage with Ollama (Local LLM)")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Create a basic symbol (syntactic by default)
        text = Symbol("Cats are adorable pets")
        print(f"Original text: {text}")
        
        # Syntactic operations (literal)
        print(f"\nSyntactic mode:")
        print(f"  'pets' in text: {'pets' in text}")
        print(f"  'dogs' in text: {'dogs' in text}")
        
        # Note: Semantic operations with local models
        print(f"\nSemantic mode with local Ollama (.sem projection):")
        print("Querying local model...")
        
        try:
            feline_check = 'feline' in text.sem
            print(f"  'feline' in text.sem: {feline_check}")
            
            animals_check = 'animals' in text.sem  
            print(f"  'animals' in text.sem: {animals_check}")
        except Exception as e:
            print(f"  ⚠️  Semantic operations failed: {e}")
            print(f"     This might be due to model or configuration issues")
        
        # Direct query to test the connection
        print(f"\nDirect query test:")
        try:
            result = text.query("Are cats considered animals? Answer yes or no.")
            print(f"  Query result: {result}")
        except Exception as e:
            print(f"  ❌ Query failed: {e}")
        
    except Exception as e:
        print(f"❌ Error in basic symbols demo: {e}")

def demo_local_text_operations():
    """Demonstrate text operations with local Ollama."""
    print("\n" + "="*60)
    print("🧮 DEMO 2: Text Operations with Local LLM")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Test composition
        print("Testing text composition...")
        idea = Symbol("artificial intelligence", semantic=True)
        
        try:
            composed = idea.compose()
            print(f"AI composition: {composed}")
        except Exception as e:
            print(f"❌ Composition failed: {e}")
        
        # Test translation
        print("\nTesting translation...")
        hello = Symbol("Hello, how are you?")
        
        try:
            german = hello.query("Translate this to German")
            print(f"German translation: {german}")
        except Exception as e:
            print(f"❌ Translation failed: {e}")
        
        # Test simple reasoning
        print("\nTesting simple reasoning...")
        math_problem = Symbol("What is 2 + 2?")
        
        try:
            answer = math_problem.query("Solve this math problem")
            print(f"Math answer: {answer}")
        except Exception as e:
            print(f"❌ Math reasoning failed: {e}")
            
    except Exception as e:
        print(f"❌ Error in text operations demo: {e}")

def demo_local_data_processing():
    """Demonstrate data processing with local model."""
    print("\n" + "="*60)
    print("📊 DEMO 3: Data Processing with Local LLM")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Sample data for processing
        animals = Symbol([
            "cat", "dog", "lion", "tiger", "goldfish", 
            "shark", "whale", "eagle", "sparrow"
        ])
        
        print(f"Animals list: {animals}")
        
        # Test data transformation
        print("\n🔄 Testing data transformation...")
        try:
            # Use a simpler approach for local models
            animal_descriptions = Symbol("cat, dog, lion").query(
                "For each animal, write one descriptive word. Format: animal=description"
            )
            print(f"Animal descriptions: {animal_descriptions}")
        except Exception as e:
            print(f"❌ Data transformation failed: {e}")
        
        # Test categorization
        print("\n📂 Testing categorization...")
        try:
            categories = Symbol("cat, dog, fish, bird").query(
                "Categorize these animals as 'domestic' or 'wild'. List each with its category."
            )
            print(f"Categories: {categories}")
        except Exception as e:
            print(f"❌ Categorization failed: {e}")
            
    except Exception as e:
        print(f"❌ Error in data processing demo: {e}")

def demo_local_model_info():
    """Display information about the local model setup."""
    print("\n" + "="*60)
    print("🤖 DEMO 4: Local Model Information")
    print("="*60)
    
    try:
        # Load configuration
        with open("symai.config.ollama.json") as f:
            config = json.load(f)
        
        print("Current Ollama Configuration:")
        print(f"  Model: {config.get('NEUROSYMBOLIC_ENGINE_MODEL', 'N/A')}")
        print(f"  Base URL: {config.get('NEUROSYMBOLIC_ENGINE_BASE_URL', 'N/A')}")
        print(f"  API Key: {config.get('NEUROSYMBOLIC_ENGINE_API_KEY', 'N/A')}")
        
        # Test model availability
        print("\n🔍 Testing model availability...")
        from symai import Symbol
        
        test_prompt = Symbol("Hello! Please respond with 'Model is working correctly.'")
        try:
            response = test_prompt.query("Just repeat the exact message I gave you.")
            print(f"Model response: {response}")
            
            if "working correctly" in str(response).lower():
                print("✅ Model is responding correctly!")
            else:
                print("⚠️  Model responded but not as expected")
                
        except Exception as e:
            print(f"❌ Model test failed: {e}")
            
        # Performance note
        print("\n💡 Performance Notes:")
        print("  • Local models may be slower than cloud APIs")
        print("  • Response quality depends on the model size and type")
        print("  • DeepSeek-R1 14B is optimized for reasoning tasks")
        print("  • Consider using GPU acceleration for better performance")
        
    except Exception as e:
        print(f"❌ Error getting model info: {e}")

def demo_troubleshooting():
    """Provide troubleshooting guidance."""
    print("\n" + "="*60)
    print("🔧 DEMO 5: Troubleshooting Guide")
    print("="*60)
    
    print("Common Issues and Solutions:")
    print("\n1. ❌ 'Cannot connect to Ollama'")
    print("   Solution: Make sure Ollama is running:")
    print("   $ ollama serve")
    
    print("\n2. ❌ 'Model not found'")
    print("   Solution: Pull the required model:")
    print("   $ ollama pull deepseek-r1:14b")
    
    print("\n3. ❌ 'Slow responses'")
    print("   Solutions:")
    print("   • Use a smaller model (e.g., llama3.2:3b)")
    print("   • Enable GPU acceleration")
    print("   • Reduce max_tokens in requests")
    
    print("\n4. ❌ 'Poor quality responses'")
    print("   Solutions:")
    print("   • Try a larger or more specialized model")
    print("   • Adjust temperature and other parameters")
    print("   • Improve prompt engineering")
    
    print("\n5. 🔄 Switching Models:")
    print("   • Edit symai.config.ollama.json")
    print("   • Change NEUROSYMBOLIC_ENGINE_MODEL")
    print("   • Restart the application")
    
    print("\n📋 Available Models (examples):")
    print("   • deepseek-r1:14b (reasoning, current)")
    print("   • llama3.2:3b (fast, lightweight)")
    print("   • llama3.1:8b (balanced)")
    print("   • codellama:7b (code-focused)")
    print("   • mistral:7b (general purpose)")

def main():
    """Main demonstration function."""
    print("🎭 SymbolicAI with Ollama (Local LLM)")
    print("=====================================")
    print("A demonstration of neuro-symbolic programming using local models")
    
    # Check setup first
    if not check_ollama_setup():
        print("\n❌ Ollama setup incomplete. Please fix the issues above.")
        print("\nQuick Setup Guide:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Pull model: ollama pull deepseek-r1:14b")
        print("3. Start server: ollama serve")
        print("4. Restart this script")
        return
    
    try:
        # Run all demonstrations
        demo_basic_symbols_ollama()
        demo_local_text_operations()
        demo_local_data_processing()
        demo_local_model_info()
        demo_troubleshooting()
        
        print("\n" + "="*60)
        print("🎉 Local Ollama Demo completed!")
        print("="*60)
        print("\n🔗 Next steps:")
        print("1. Experiment with different models in symai.config.ollama.json")
        print("2. Try more complex neuro-symbolic operations")
        print("3. Build your own local AI applications")
        print("4. Explore SymbolicAI's advanced features")
        print("\n💡 Benefits of Local LLMs:")
        print("   ✅ Privacy: Your data stays on your machine")
        print("   ✅ Cost: No API fees or rate limits") 
        print("   ✅ Control: Full control over the model and parameters")
        print("   ✅ Offline: Works without internet connection")
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure SymbolicAI is properly installed.")
        print("Run: ./symbolicai/bin/pip install symbolicai")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Check your configuration and Ollama setup.")

if __name__ == "__main__":
    main()