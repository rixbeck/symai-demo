#!/usr/bin/env python3
"""
Simple test script to verify SymbolicAI setup
"""

def test_basic_import():
    """Test if SymbolicAI imports correctly."""
    try:
        import symai
        from symai import Symbol
        print("✅ SymbolicAI imports successfully")
        print(f"   Version: {symai.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_symbol():
    """Test basic Symbol functionality."""
    try:
        from symai import Symbol
        
        # Test syntactic mode
        s = Symbol("Hello World")
        print("✅ Basic Symbol creation works")
        
        # Test string operations
        result = str(s)
        print(f"   Symbol content: {result}")
        
        return True
    except Exception as e:
        print(f"❌ Symbol test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    try:
        import json
        from pathlib import Path
        
        config_path = Path("symai.config.json")
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
            
            api_key = config.get("NEUROSYMBOLIC_ENGINE_API_KEY", "")
            if api_key and api_key != "<YOUR_OPENAI_API_KEY>":
                print("✅ Configuration file found and API key is set")
            else:
                print("⚠️  API key not configured - semantic operations won't work")
                print("   Edit symai.config.json to add your OpenAI API key")
            
            return True
        else:
            print("❌ Configuration file not found")
            return False
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔧 Testing SymbolicAI Setup")
    print("=" * 40)
    
    tests = [
        test_basic_import,
        test_basic_symbol, 
        test_configuration
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 Setup is complete! You can run the main demo:")
        print("   ./symbolicai/bin/python main.py")
    else:
        print("⚠️  Some issues found. Check the errors above.")

if __name__ == "__main__":
    main()