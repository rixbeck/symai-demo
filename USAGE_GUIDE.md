# SymbolicAI Demo - Usage Guide

## Overview
This guide explains how to use the refactored SymbolicAI demo application with its new modular structure.

## Quick Start

### Running the Main Demo
```bash
# Run with Ollama (local)
python main.py ollama

# Run with OpenAI Compatible (cloud)
python main.py openai-comp
```

### Running Tests
```bash
# Basic setup verification
python -m src.tests.test_setup

# Engine integration tests
python test_engine.py ollama
python test_engine.py openai-comp
```

### Running Debug Scripts
```bash
# Debug Ollama integration
python -m src.debug.debug_ollama

# Debug query content
python -m src.debug.debug_query_content

# Debug symbol display
python -m src.debug.test_symbol_display
```

## Module Structure

### `src/` - Main Package
```
src/
├── __init__.py              # Package documentation
├── engines/                 # Engine management
├── demos/                   # Demo functions
├── tests/                   # Test scripts
├── debug/                   # Debug utilities
└── utils/                   # Configuration utilities
```

### `src/engines/` - Engine Management
- **`engine_manager.py`**: Centralized engine setup and management
- **`openai_engine.py`**: OpenAI engine implementation
- **`ollama_engine.py`**: Ollama engine implementation

### `src/demos/` - Demo Functions
- **`demos.py`**: All 7 demo functions:
  - `demo_basic_symbols()`
  - `demo_symbol_operations()`
  - `demo_data_processing()`
  - `demo_contracts_basic()`
  - `demo_configuration()`
  - `demo_embeddings()`
  - `demo_advanced_features()`

### `src/tests/` - Test Scripts
- **`test_setup.py`**: Basic setup and import verification
- **`test_engine.py`**: Comprehensive engine integration tests

### `src/debug/` - Debug Utilities
- **`debug_ollama.py`**: Ollama engine debugging
- **`debug_query_content.py`**: Query content inspection
- **`test_symbol_display.py`**: Symbol object debugging

### `src/utils/` - Utilities
- **`config.py`**: Engine configuration management

## Usage Examples

### Importing Modules

```python
# Import demo functions
from src.demos.demos import demo_basic_symbols, demo_embeddings

# Import engine manager
from src.engines.engine_manager import EngineManager

# Import configuration utilities
from src.utils.config import ENGINE_CONFIGS, get_engine_config
```

### Using Engine Manager Programmatically

```python
from src.engines.engine_manager import EngineManager

# Setup Ollama engine
success = EngineManager.setup_engine('ollama')
if success:
    print("Engine ready!")

# Test connection
if EngineManager.test_engine_connection('ollama'):
    print("Connection successful!")
```

### Running Individual Demo Functions

```python
from src.demos import demos
from src.engines.engine_manager import EngineManager

# Setup engine
EngineManager.setup_engine('ollama')

# Share engine state with demos
demos.current_engine = {
    'type': 'ollama',
    'config': {'display_name': 'Ollama'}
}

# Run specific demo
demos.demo_basic_symbols()
```

## Configuration

### Engine Configuration Files
- **`symai.config.openai.json`**: OpenAI configuration
- **`symai.config.ollama.json`**: Ollama configuration
- **`symai.config.json`**: General configuration (deprecated)

### Environment Variables
All configuration can be overridden with environment variables:
- `NEUROSYMBOLIC_ENGINE_API_KEY`
- `NEUROSYMBOLIC_ENGINE_MODEL`
- `NEUROSYMBOLIC_ENGINE_BASE_URL`

## Migration from Old Structure

### Old Commands → New Commands
```bash
# Old
python test_engine.py ollama
python -m src.debug.debug_ollama

# New
python -m src.tests.test_engine ollama
python -m src.debug.debug_ollama
```

### Old Imports → New Imports
```python
# Old
from engine_manager import EngineManager
import debug_ollama

# New
from src.engines.engine_manager import EngineManager
from src.debug import debug_ollama
```

## Troubleshooting

### Import Errors
If you get import errors, make sure you're running from the project root directory and using the correct module syntax:
```bash
# Correct
python -m src.tests.test_setup

# Incorrect
python src/tests/test_setup.py
```

### Module Not Found
Ensure all `__init__.py` files are present:
```bash
find src/ -name "__init__.py"
```

### Engine Setup Issues
Use the debug scripts to diagnose engine problems:
```bash
python -m src.debug.debug_ollama
python -m src.tests.test_setup
```

## Development

### Adding New Demo Functions
1. Add function to `src/demos/demos.py`
2. Import required dependencies locally within the function
3. Update main.py to call the new demo function

### Adding New Test Scripts
1. Create new test file in `src/tests/`
2. Use relative imports: `from ..engines.engine_manager import EngineManager`
3. Add module execution support: `if __name__ == "__main__": main()`

### Adding New Debug Scripts
1. Create new debug file in `src/debug/`
2. Follow the same patterns as existing debug scripts
3. Include comprehensive error handling and diagnostics

## Best Practices

1. **Use Module Execution**: Always run scripts using `python -m` syntax
2. **Relative Imports**: Use relative imports within the package
3. **Error Handling**: Include comprehensive error handling in all scripts
4. **Documentation**: Document all functions and modules clearly
5. **Testing**: Test all functionality before committing changes

## Support

For issues or questions about the refactored structure:
1. Check the troubleshooting section above
2. Run the setup test: `python -m src.tests.test_setup`
3. Review the refactoring summary: `REFACTORING_SUMMARY.md`