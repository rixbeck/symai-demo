# SymbolicAI Engine Testing Guide

This document explains how to test different engine integrations for SymbolicAI.

## Quick Start

Test a specific engine using:
```bash
python test_engine.py [engine_type]
```

Available engines:
- `openai`: Test OpenAI or compatible endpoint
- `ollama`: Test local Ollama integration

## Configuration

Each engine requires its own configuration file:

1. OpenAI: `symai.config.openai.json`
```json
{
    "NEUROSYMBOLIC_ENGINE_BASE_URL": "https://api.openai.com/v1",
    "NEUROSYMBOLIC_ENGINE_MODEL": "gpt-4",
    "NEUROSYMBOLIC_ENGINE_API_KEY": "your-api-key"
}
```

2. Ollama: `symai.config.ollama.json`
```json
{
    "NEUROSYMBOLIC_ENGINE_BASE_URL": "http://localhost:11434/v1",
    "NEUROSYMBOLIC_ENGINE_MODEL": "deepseek-r1:14b",
    "NEUROSYMBOLIC_ENGINE_API_KEY": "ollama"
}
```

## Test Cases

The test suite includes:

1. Basic Query Test
   - Simple query execution
   - Response validation
   - Error handling

2. Context Handling Test
   - Context-aware queries
   - Response formatting
   - Word count validation

3. Performance Test
   - Multiple queries
   - Response time measurement
   - Success rate calculation

## Troubleshooting

### OpenAI Issues
- Verify API key is valid
- Check internet connection
- Confirm API endpoint is accessible

### Ollama Issues
- Ensure Ollama server is running (`ollama serve`)
- Verify required model is installed (`ollama pull modelname`)
- Check local endpoint accessibility

## Adding New Engines

To add support for a new engine:

1. Add engine configuration to `ENGINE_CONFIGS` in test_engine.py
2. Create corresponding configuration file
3. Implement engine-specific connection testing
4. Run test suite to verify integration

## Exit Codes
- 0: All tests passed
- 1: Test failures or configuration issues