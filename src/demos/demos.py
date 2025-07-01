from typing import Dict, Any
from pathlib import Path
import json

# Global engine state (will be imported from main)
current_engine: Dict[str, Any] = {'type': None, 'config': None}

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
    print("📊 DEMO 3: Data Processing and Analysis")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Sample data for processing
        animals = Symbol([
            "cat", "dog", "lion", "tiger", "goldfish",
            "shark", "whale", "eagle", "sparrow", "penguin"
        ])
        
        print(f"Animals list: {animals}")
        
        # Group animals by type using semantic filtering
        print("\n🔍 Finding mammals in the list...")
        mammals = animals.filter("find all mammals")
        print(f"Mammals: {mammals}")
        
        print("\n🐟 Finding aquatic animals...")
        aquatic = animals.filter("find all aquatic animals")
        print(f"Aquatic animals: {aquatic}")
        
        print("\n🦅 Finding birds...")
        birds = animals.filter("find all birds")
        print(f"Birds: {birds}")
        
        # Demonstrate simple classification
        print("\n🏷️ Classifying by habitat...")
        habitats = Symbol(animals).query("classify each animal by their typical habitat (land, water, or air)")
        print(f"Habitat classification:\n{habitats}")
        
    except Exception as e:
        print(f"❌ Error in data processing demo: {e}")
        print(f"   Using {current_engine['config']['display_name']} backend")

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

def demo_embeddings():
    """Demonstrate embedding generation and vector operations."""
    print("\n" + "="*60)
    engine_name = current_engine['config']['display_name']
    print(f"🧬 DEMO 6: Embeddings with {engine_name}")
    print("="*60)
    
    try:
        from symai import Symbol
        
        # Create test symbols with semantic understanding
        text1 = Symbol("The cat chases the mouse", semantic=True)
        text2 = Symbol("A feline pursues a rodent", semantic=True)
        text3 = Symbol("The dog barks at the mailman", semantic=True)
        
        # Demonstrate semantic matching
        print("Testing semantic relationships...")
        print(f"\nComparing similar concepts:")
        print(f"Text 1: '{text1}'")
        print(f"Text 2: '{text2}'")
        print(f"Semantic match: {text1.sem == text2.sem}")
        
        print(f"\nComparing different concepts:")
        print(f"Text 1: '{text1}'")
        print(f"Text 3: '{text3}'")
        print(f"Semantic match: {text1.sem == text3.sem}")
        
        # Demonstrate semantic search
        print("\n🔍 Testing semantic search...")
        corpus = Symbol([
            "The sun is shining brightly today",
            "Heavy rain falls from dark clouds",
            "A beautiful sunny morning in the park",
            "Thunder and lightning fill the stormy sky",
            "Children play under the warm sunlight"
        ])
        
        # Search using semantic understanding
        query = Symbol("good weather", semantic=True)
        print(f"\nSearching for: '{query}'")
        results = corpus.filter("find texts about good weather")
        print("Top matches:")
        for idx, result in enumerate(results[:2], 1):
            print(f"  {idx}. {result}")
        
        # Display capabilities
        print(f"\n🔬 {engine_name} Semantic Features:")
        if current_engine['type'] == 'openai-comp':
            print("  • Advanced semantic understanding")
            print("  • Cross-lingual capabilities")
            print("  • Context-aware matching")
            print("  • Cloud-based processing")
        else:
            print("  • Local semantic processing")
            print("  • Pattern matching")
            print("  • Text similarity detection")
            print("  • No API costs")
        
    except Exception as e:
        print(f"❌ Error in embeddings demo: {e}")
        print(f"   Please verify your {engine_name} setup and try again")

def demo_advanced_features():
    """Demonstrate advanced features briefly."""
    print("\n" + "="*60)
    engine_name = current_engine['config']['display_name']
    print(f"🚀 DEMO 7: Advanced Features with {engine_name}")
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
        if current_engine['type'] == 'openai-comp':
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