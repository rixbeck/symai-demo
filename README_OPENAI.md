# OpenAI Engine for SymbolicAI

This implementation provides OpenAI API support for SymbolicAI, allowing you to use either OpenAI's official API or local/custom OpenAI-compatible API providers.

## Features

- Support for both OpenAI API and local OpenAI-compatible endpoints
- Chat completions endpoint integration
- Configurable model and API parameters
- Built-in thinking tag handling
- Comprehensive error handling
- Test suite with endpoint detection

## Setup

### Using OpenAI API

1. Copy `symai.config.openai.json` and configure for OpenAI:
   ```json
   {
       "NEUROSYMBOLIC_ENGINE_BASE_URL": "https://api.openai.com/v1",
       "NEUROSYMBOLIC_ENGINE_MODEL": "gpt-4",
       "NEUROSYMBOLIC_ENGINE_API_KEY": "your-openai-api-key-here",
       "EMBEDDING_ENGINE_API_KEY": "your-openai-api-key-here",
       "EMBEDDING_ENGINE_MODEL": "text-embedding-3-small",
       "TEXT_TO_SPEECH_ENGINE_API_KEY": "your-openai-api-key-here"
   }
   ```

### Using Local/Custom OpenAI-Compatible Endpoint

1. Configure for your local endpoint:
   ```json
   {
       "NEUROSYMBOLIC_ENGINE_BASE_URL": "http://localhost:8000",
       "NEUROSYMBOLIC_ENGINE_MODEL": "your-model-name",
       "NEUROSYMBOLIC_ENGINE_API_KEY": "your-local-api-key",
       "EMBEDDING_ENGINE_API_KEY": "your-local-api-key",
       "EMBEDDING_ENGINE_MODEL": "your-embedding-model",
       "TEXT_TO_SPEECH_ENGINE_API_KEY": "your-local-api-key"
   }
   ```

### Implementation

1. Import and set up the engine:
   ```python
   from openai_engine import setup_openai_engine
   
   # Setup the engine with your configuration
   setup_openai_engine("symai.config.openai.json")
   ```

2. Use SymbolicAI normally:
   ```python
   from symai import Symbol
   
   # Create and use symbols
   symbol = Symbol("Hello!")
   response = symbol.query("Say hi!")
   print(response)
   ```

## Testing

Run the unified test suite to verify your setup:

```bash
python test_engine.py openai
```

The test script will:
1. Detect if you're using OpenAI API or a local endpoint
2. Check API connectivity
3. Verify engine setup
4. Run basic query tests
5. Test context handling
6. Perform performance benchmarking

For more details on testing, see [TEST_README.md](TEST_README.md)

## Configuration Options

- `NEUROSYMBOLIC_ENGINE_BASE_URL`: API endpoint URL (OpenAI or local)
- `NEUROSYMBOLIC_ENGINE_MODEL`: Model to use
- `NEUROSYMBOLIC_ENGINE_API_KEY`: API key for authentication

## Advanced Usage

### Local Development Setup

For local development or testing with OpenAI-compatible servers:

```python
from openai_engine import OpenAIEngine
from symai.functional import EngineRepository

# Create engine with local endpoint
engine = OpenAIEngine(
    base_url="http://localhost:8000",
    model="local-model",
    api_key="local-key"
)

# Register the engine
EngineRepository.register('neurosymbolic', engine)
```

### Debug Mode

Enable verbose output for debugging:

```python
engine = OpenAIEngine()
engine.verbose = True
```

## Error Handling

The engine includes comprehensive error handling for:
- API connection issues
- Authentication errors
- Invalid responses
- Rate limiting
- Network timeouts

Errors are logged and returned as error messages in the response.

## Compatibility

This implementation is compatible with:
- OpenAI API
- Azure OpenAI Service
- Local OpenAI-compatible servers
- Custom API endpoints following OpenAI's format

## Requirements

- Python 3.8+
- `requests` library
- SymbolicAI base installation
- Either:
  - Valid OpenAI API key, or
  - Access to a local/custom OpenAI-compatible endpoint

## Troubleshooting

### OpenAI API Issues
- Verify your API key is valid
- Check your OpenAI account subscription status
- Ensure the requested model is available for your account

### Local Endpoint Issues
- Verify your local server is running
- Check the endpoint URL is correct
- Confirm the API key matches your local setup
- Ensure your model name matches what's available locally