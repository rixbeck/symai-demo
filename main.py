#!/usr/bin/env python3
"""
SymbolicAI Playground - Basic Demonstration
===========================================

This script demonstrates the core features of SymbolicAI:
1. Symbol objects (syntactic vs semantic modes)
2. Basic primitives and operations
3. Contracts and validation
4. Configuration management

Before running:
1. Set your OpenAI API key in symai.config.json
2. Run: ./symbolicai/bin/python main.py
"""

import os
import sys
from pathlib import Path

def check_setup():
    """Check if the setup is correct before proceeding."""
    print("🔧 Checking SymbolicAI setup...")
    
    # Check if config file exists
    config_path = Path("symai.config.json")
    if not config_path.exists():
        print("❌ Configuration file 'symai.config.json' not found!")
        return False
    
    # Check if API key is set
    import json
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        api_key = config.get("NEUROSYMBOLIC_ENGINE_API_KEY", "")
        if api_key == "<YOUR_OPENAI_API_KEY>" or not api_key:
            print("⚠️  Please set your OpenAI API key in symai.config.json")
            print("   Replace '<YOUR_OPENAI_API_KEY>' with your actual API key")
            return False
        
        print("✅ Configuration looks good!")
        return True
    except Exception as e:
        print(f"❌ Error reading config: {e}")
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
    print("🧮 DEMO 2: Symbol Operations and Arithmetic")
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
    print("⚙️  DEMO 5: Configuration Management")
    print("="*60)
    
    try:
        # Show current configuration
        import json
        with open("symai.config.json") as f:
            config = json.load(f)
        
        print("Current configuration:")
        for key, value in config.items():
            if "API_KEY" in key:
                # Mask API key for security
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: {value}")
                
        print("\n📍 Configuration file location: ./symai.config.json")
        print("📍 You can also use environment variables or global config in ~/.symai/")
        
    except Exception as e:
        print(f"❌ Error in configuration demo: {e}")

def demo_advanced_features():
    """Demonstrate advanced features briefly."""
    print("\n" + "="*60)
    print("🚀 DEMO 6: Advanced Features Overview")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Similarity comparison
        text1 = Symbol("Machine learning is fascinating", semantic=True)
        text2 = Symbol("AI is amazing", semantic=True)
        
        similarity = text1.similarity(text2)
        print(f"Similarity between texts: {similarity}")
        
        # Choice selection
        options = ["red", "blue", "green", "yellow"]
        color_symbol = Symbol(options)
        chosen = color_symbol.choice(["warm color", "cool color", "nature color"], default="blue")
        print(f"Chosen color based on 'nature color': {chosen}")
        
        print("\n🌟 Other advanced features available:")
        print("  • Web search integration (with SERP API)")
        print("  • Image processing (with vision models)")
        print("  • Speech-to-text (with Whisper)")
        print("  • PDF processing")
        print("  • Vector embeddings and similarity search")
        print("  • Custom engine development")
        
    except Exception as e:
        print(f"❌ Error in advanced features demo: {e}")

def main():
    """Main demonstration function."""
    print("🎭 SymbolicAI Playground")
    print("=======================")
    print("A comprehensive demonstration of neuro-symbolic programming with LLMs")
    
    # Check setup first
    if not check_setup():
        print("\n❌ Setup incomplete. Please configure your API key first.")
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
        print("🎉 Demo completed successfully!")
        print("="*60)
        print("\n🔗 Next steps:")
        print("1. Explore the official documentation: https://extensityai.gitbook.io/symbolicai")
        print("2. Check out examples: https://github.com/ExtensityAI/symbolicai/tree/main/examples")
        print("3. Read the research paper: https://arxiv.org/abs/2402.00854")
        print("4. Try building your own neuro-symbolic applications!")
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure SymbolicAI is properly installed.")
        print("Run: ./symbolicai/bin/pip install symbolicai")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Check your configuration and try again.")

if __name__ == "__main__":
    main()