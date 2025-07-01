# SymbolicAI Engine Testing Guide

This document explains how to test different engine integrations for SymbolicAI, ensuring your configuration is valid and the connection to your chosen backend (OpenAI or Ollama) is working correctly.

## 🚀 Quick Test

To validate your setup for a specific engine, run the unified test script from the project root:

```bash
# General usage
./symbolicai/bin/python test_engine.py [engine_type]

# --- Examples ---

# Test OpenAI Compatible setup
./symbolicai/bin/python test_engine.py openai-comp

# Test Ollama setup
./symbolicai/bin/python test_engine.py ollama
```

## ✅ What the Test Suite Verifies

The test suite will automatically perform the following checks:

-   **Configuration Validity**: Reads and parses your `symai.config.[engine].json` file.
-   **API/Server Accessibility**: Attempts to connect to the configured endpoint (OpenAI API or local Ollama server).
-   **Basic Query Functionality**: Sends a simple query and validates that a coherent response is received.
-   **Context Handling**: Checks if the engine can process context-aware queries.
-   **Performance Benchmarks**: Measures response times for a series of queries to give a basic performance indication.

## ⚙️ Configuration

The test script relies on the same configuration files used by the main application. Ensure the correct file is present and configured in the project's root directory.

### OpenAI Compatible Configuration (`symai.config.openai.json`)

```json
{
    "NEUROSYMBOLIC_ENGINE_API_KEY": "sk-your-actual-api-key-here",
    "NEUROSYMBOLIC_ENGINE_MODEL": "gpt-4o-mini",
    "EMBEDDING_ENGINE_API_KEY": "sk-your-actual-api-key-here",
    "EMBEDDING_ENGINE_MODEL": "text-embedding-3-small"
}
```

### Ollama Configuration (`symai.config.ollama.json`)

```json
{
    "NEUROSYMBOLIC_ENGINE_API_KEY": "ollama",
    "NEUROSYMBOLIC_ENGINE_MODEL": "deepseek-r1:14b",
    "NEUROSYMBOLIC_ENGINE_BASE_URL": "http://localhost:11434/v1",
    "EMBEDDING_ENGINE_API_KEY": "ollama",
    "EMBEDDING_ENGINE_MODEL": "nomic-embed-text",
    "EMBEDDING_ENGINE_BASE_URL": "http://localhost:11434/v1"
}
```

## 🐛 Troubleshooting Test Failures

### OpenAI Compatible Issues

-   **API Key Error**: Verify your API key in `symai.config.openai.json` is valid and has sufficient credits.
-   **Connection Error**: Check your internet connection. Ensure `https://api.openai.com` is accessible.
-   **Model Error**: Make sure the model you specified (e.g., `gpt-4o-mini`) is available for your API key.

### Ollama Issues

-   **Connection Error**: Ensure the Ollama server is running. You can start it with `ollama serve`.
-   **Model Not Found**: Pull the required model using `ollama pull <model_name>` (e.g., `ollama pull deepseek-r1:14b`).
-   **Performance**: If tests are slow, try a lighter model like `llama3.2:3b`.

## 📈 Exit Codes

-   **0**: All tests passed successfully.
-   **1**: One or more tests failed, or there was a configuration issue.