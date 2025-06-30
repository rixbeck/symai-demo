#!/usr/bin/env python3
"""
SymbolicAI Playground - Basic Demonstration
===========================================

This script demonstrates the core features of SymbolicAI using either:
- OpenAI's cloud-based API
- Local Ollama LLM integration

Usage:
    python main.py [openai|ollama]

Example:
    python main.py openai    # Run with OpenAI
    python main.py ollama    # Run with Ollama
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Global engine state
current_engine: Dict[str, Any] = {'type': None, 'config': None}

ENGINE_CONFIGS = {
    'openai': {
        'config_file': 'symai.config.openai.json',
        'display_name': 'OpenAI',
        'setup_message': 'Cloud-based OpenAI API',
    },
    'ollama': {
        'config_file': 'symai.config.ollama.json',
        'display_name': 'Ollama',
        'setup_message': 'Local Ollama LLM',
    }
}

def check_setup(engine_type: str):
    """Check if the setup is correct before proceeding."""
    if engine_type not in ENGINE_CONFIGS:
        print(f"❌ Unknown engine type: {engine_type}")
        print("Available engines:", ", ".join(ENGINE_CONFIGS.keys()))
        return False

    config = ENGINE_CONFIGS[engine_type]
    print(f"🔧 Checking SymbolicAI setup for {config['display_name']}...")
    print(f"Using {config['setup_message']}")
    
    from engine_manager import EngineManager
    
    if EngineManager.setup_engine(engine_type, config_path=config['config_file']):
        print(f"✅ {config['display_name']} configuration and setup successful!")
        return True
        
    print(f"❌ {config['display_name']} setup failed - please check your configuration.")
    return False

def demo_basic_symbols():
    """Demonstrate basic Symbol usage - syntactic vs semantic."""
    print("\n" + "="*60)
    print("📝 DEMO 1: Basic Symbol Usage (Syntactic vs Semantic)")
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
        
        # Semantic operations (meaning-based)
        print(f"\nSemantic mode (.sem projection):")
        print(f"  'feline' in text.sem: {'feline' in text.sem}")
        print(f"  'animals' in text.sem: {'animals' in text.sem}")
        
        # Create semantic symbol directly
        semantic_text = Symbol("Python is a great programming language", semantic=True)
        print(f"\nSemantic symbol: {semantic_text}")
        print(f"  'coding' in semantic_text: {'coding' in semantic_text}")
        
    except Exception as e:
        print(f"❌ Error in basic symbols demo: {e}")
        print("Make sure your API key is set correctly in symai.config.json")

def demo_symbol_operations():
    """Demonstrate Symbol arithmetic and logical operations."""
    print("\n" + "="*60)
    engine_name = current_engine['config']['display_name']
    print(f"🧮 DEMO 2: Symbol Operations with {engine_name}")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Semantic addition (composition)
        idea1 = Symbol("artificial intelligence", semantic=True)
        idea2 = Symbol("creativity", semantic=True)
        combined = idea1 + idea2
        print(f"AI + Creativity = {combined}")
        
        # Semantic equality (fuzzy matching)
        greeting1 = Symbol("Hello there!", semantic=True)
        greeting2 = Symbol("Hi!", semantic=True)
        print(f"\n'Hello there!' == 'Hi!' (semantic): {greeting1 == greeting2}")
        
        # List operations
        fruits = Symbol(['apple', 'banana', 'cherry'])
        print(f"\nOriginal fruits: {fruits}")
        
        # Map operation (semantic transformation)
        vegetables = fruits.map('convert all fruits to vegetables')
        print(f"Converted to vegetables: {vegetables}")
        
    except Exception as e:
        print(f"❌ Error in operations demo: {e}")

def demo_data_processing():
    """Demonstrate data processing capabilities."""
    print("\n" + "="*60)
    print("📊 DEMO 3: Data Processing and Clustering")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Sample data for processing
        animals = Symbol([
            "cat", "dog", "lion", "tiger", "goldfish", 
            "shark", "whale", "eagle", "sparrow", "penguin"
        ])
        
        print(f"Animals list: {animals}")
        
        # Semantic clustering
        print("\n🔍 Clustering animals by type...")
        clusters = animals.cluster()
        print(f"Clustered groups: {clusters}")
        
        # Conditional processing
        print("\n🐾 Processing with conditions...")
        mammals = animals.foreach("if animal is a mammal", "mark as mammal")
        print(f"Mammal analysis: {mammals}")
        
    except Exception as e:
        print(f"❌ Error in data processing demo: {e}")

def demo_contracts_basic():
    """Demonstrate basic contract validation."""
    print("\n" + "="*60)
    print("📋 DEMO 4: Basic Contracts and Validation")
    print("="*60)
    
    try:
        from symai import Expression
        from symai.strategy import contract
        from pydantic import BaseModel, Field
        
        # Simple data model
        class TaskModel(BaseModel):
            title: str = Field(description="A clear, concise task title")
            priority: str = Field(description="Priority level: high, medium, or low")
            category: str = Field(description="Task category like 'work', 'personal', 'study'")
        
        # Contract-based expression
        @contract(
            pre_remedy=True,
            post_remedy=True,
            verbose=True
        )
        class TaskAnalyzer(Expression):
            prompt = "Analyze the given text and extract task information."
            
            def forward(self, text, **kwargs):
                # This would normally call the LLM
                # For demo purposes, return a mock response
                return TaskModel(
                    title="Sample Task",
                    priority="medium", 
                    category="demo"
                )
        
        # Create and test the analyzer
        analyzer = TaskAnalyzer()
        print("✅ Contract-based TaskAnalyzer created successfully!")
        print("   This demonstrates the structure for validation and remediation.")
        
    except Exception as e:
        print(f"❌ Error in contracts demo: {e}")

def demo_configuration():
    """Demonstrate configuration management."""
    print("\n" + "="*60)
    engine_name = current_engine['config']['display_name']
    print(f"⚙️  DEMO 5: {engine_name} Configuration Management")
    print("="*60)
    
    try:
        # Show current configuration
        config_file = current_engine['config']['config_file']
        with open(config_file) as f:
            config = json.load(f)
        
        print(f"Current {engine_name} configuration:")
        for key, value in config.items():
            if "API_KEY" in key:
                # Mask API key for security
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: {value}")
                
        print(f"\n📍 Configuration file location: ./{config_file}")
        print("📍 You can also use environment variables or global config in ~/.symai/")
        
    except Exception as e:
        print(f"❌ Error in configuration demo: {e}")
        print(f"   Please check {config_file} exists and is valid JSON")

def demo_advanced_features():
    """Demonstrate advanced features briefly."""
    print("\n" + "="*60)
    engine_name = current_engine['config']['display_name']
    print(f"🚀 DEMO 6: Advanced Features with {engine_name}")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Simple transformation demo
        print("Testing semantic transformation...")
        text = Symbol("Today is a very cold day", semantic=True)
        transformed = text.query("Transform this statement to describe the opposite weather")
        print(f"Original: {text}")
        print(f"Transformed: {transformed}")
        
        # Basic classification
        print("\nTesting classification...")
        foods = Symbol(["pizza", "apple", "ice cream", "carrot"])
        print(f"Foods: {foods}")
        categories = foods.query("Classify each food as 'healthy' or 'treat'")
        print(f"Classifications: {categories}")
        
        print("\n🌟 Available features with your setup:")
        if current_engine['type'] == 'openai':
            print("  • Access to latest GPT models")
            print("  • Cloud-based processing")
            print("  • Integration with OpenAI services")
        else:
            print("  • Local processing with no API costs")
            print("  • Full privacy and control")
            print("  • Customizable model selection")
            
        print("\n💡 Common capabilities:")
        print("  • Text generation and transformation")
        print("  • Classification and analysis")
        print("  • Natural language processing")
        print("  • Custom prompt engineering")
        
    except Exception as e:
        print(f"\n❌ Error in advanced features demo: {e}")
        print(f"   Please verify your {engine_name} setup and try again")

def main():
    """Main demonstration function."""
    global current_engine

    # Parse command-line argument
    if len(sys.argv) != 2 or sys.argv[1] not in ENGINE_CONFIGS:
        print("Usage: python main.py [openai|ollama]")
        print("\nAvailable engines:")
        for engine, config in ENGINE_CONFIGS.items():
            print(f"  • {engine:<10} - {config['setup_message']}")
        return

    # Set global engine state
    current_engine['type'] = sys.argv[1]
    current_engine['config'] = ENGINE_CONFIGS[current_engine['type']]
    
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
        demo_basic_symbols()
        demo_symbol_operations()
        demo_data_processing()
        demo_contracts_basic()
        demo_configuration()
        demo_advanced_features()
        
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