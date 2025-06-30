# SymbolicAI with Ollama - Local LLM Integration

A comprehensive setup for running SymbolicAI with local Ollama models, providing complete privacy and no API costs.

## 🚀 Quick Start

### 1. Install Ollama

```bash
# Linux/MacOS
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from: https://ollama.ai/
```

### 2. Pull a Model

```bash
# Pull DeepSeek-R1 14B (reasoning optimized)
ollama pull deepseek-r1:14b

# Alternative models:
ollama pull llama3.2:3b      # Lightweight, fast
ollama pull llama3.1:8b      # Balanced performance
ollama pull codellama:7b     # Code-focused
```

### 3. Start Ollama Server

```bash
ollama serve
```

### 4. Test the Integration

```bash
./symbolicai/bin/python test_engine.py ollama
```

See [TEST_README.md](TEST_README.md) for detailed testing information.

### 5. Run the Demo

```bash
./symbolicai/bin/python main_ollama.py
```

## 📁 Project Structure

```
symbolicai-playground/
├── symbolicai/                    # Conda environment
├── symai.config.ollama.json      # Ollama configuration
├── ollama_engine.py               # Custom Ollama engine
├── main_ollama.py                 # Ollama demonstration script
├── test_ollama.py                 # Integration test suite
├── README_OLLAMA.md               # This file
└── ... (other files)
```

## ⚙️ Configuration

### Ollama Configuration (`symai.config.ollama.json`)

```json
{
    "NEUROSYMBOLIC_ENGINE_API_KEY": "ollama",
    "NEUROSYMBOLIC_ENGINE_MODEL": "deepseek-r1:14b",
    "NEUROSYMBOLIC_ENGINE_BASE_URL": "http://localhost:11434/v1",
    "EMBEDDING_ENGINE_API_KEY": "ollama", 
    "EMBEDDING_ENGINE_MODEL": "nomic-embed-text",
    "EMBEDDING_ENGINE_BASE_URL": "http://localhost:11434/v1",
    "SUPPORT_COMMUNITY": false
}
```

### Model Selection

| Model | Size | Use Case | Performance |
|-------|------|----------|-------------|
| `deepseek-r1:14b` | ~8GB | Reasoning, complex tasks | High quality, slower |
| `llama3.1:8b` | ~4.7GB | General purpose | Balanced |
| `llama3.2:3b` | ~2GB | Fast responses | Quick, lower quality |
| `codellama:7b` | ~3.8GB | Programming tasks | Code-optimized |

## 🎯 What You Can Do

### Basic Operations

```python
from symai import Symbol

# Create symbols
text = Symbol("Cats are adorable pets")

# Syntactic operations (local, fast)
print("pets" in text)  # True

# Semantic operations (uses local LLM)
print("feline" in text.sem)  # True (via local model)

# Direct queries
result = text.query("Are cats considered animals?")
print(result)
```

### Advanced Features

```python
# Text generation
idea = Symbol("artificial intelligence")
composition = idea.compose()

# Translation
hello = Symbol("Hello, how are you?")
german = hello.query("Translate this to German")

# Data processing
animals = Symbol(["cat", "dog", "lion", "tiger"])
categories = animals.query("Categorize as domestic or wild")

# Reasoning
problem = Symbol("What is 2 + 2 * 3?")
solution = problem.query("Solve step by step")
```

## 🔧 Custom Engine Implementation

The `ollama_engine.py` provides a custom SymbolicAI engine that:

- **Translates** SymbolicAI requests to Ollama's OpenAI-compatible API
- **Handles** authentication and request formatting
- **Provides** error handling and fallback behavior
- **Supports** all standard OpenAI API parameters

Key features:
- OpenAI-compatible API integration
- Automatic request/response handling
- Configurable endpoints and models
- Comprehensive error handling

## 🚀 Performance Optimization

### Hardware Recommendations

- **CPU**: Modern multi-core processor (8+ cores recommended)
- **RAM**: 16GB+ (32GB for larger models)
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **Storage**: SSD with 20GB+ free space

### Speed Optimization

```bash
# Use GPU acceleration (if available)
CUDA_VISIBLE_DEVICES=0 ollama serve

# Use smaller models for faster responses
ollama pull llama3.2:3b

# Optimize for your hardware
export OLLAMA_NUM_PARALLEL=4
export OLLAMA_MAX_LOADED_MODELS=2
```

### Model-Specific Settings

```python
# In your code, you can adjust parameters:
result = text.query(
    "Your question here",
    temperature=0.1,    # Lower = more deterministic
    max_tokens=100,     # Limit response length
    top_p=0.9          # Nucleus sampling
)
```

## 🐛 Troubleshooting

### Common Issues

#### 1. "Cannot connect to Ollama"
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Check port
netstat -tulpn | grep 11434
```

#### 2. "Model not found"
```bash
# List available models
ollama list

# Pull required model
ollama pull deepseek-r1:14b
```

#### 3. "Slow responses"
```bash
# Use a smaller model
ollama pull llama3.2:3b

# Update config to use smaller model
# Edit symai.config.ollama.json:
# "NEUROSYMBOLIC_ENGINE_MODEL": "llama3.2:3b"
```

#### 4. "Out of memory"
```bash
# Check system resources
free -h
top

# Use a smaller model or increase swap
sudo swapon --show
```

#### 5. "Permission denied"
```bash
# Check Ollama permissions
sudo chmod +x $(which ollama)

# Or reinstall Ollama
curl -fsSL https://ollama.ai/install.sh | sh
```

### Debug Mode

Run tests with verbose output:

```bash
./symbolicai/bin/python -c "
import logging
logging.basicConfig(level=logging.DEBUG)

from test_ollama import main
main()
"
```

## 🔒 Privacy & Security

### Benefits of Local Deployment

- ✅ **Complete Privacy**: Your data never leaves your machine
- ✅ **No API Costs**: Run unlimited queries for free
- ✅ **Offline Operation**: Works without internet connection
- ✅ **Full Control**: Choose your models and parameters
- ✅ **No Rate Limits**: Process as much as your hardware allows

### Security Considerations

- Local models are not connected to external services
- All processing happens on your machine
- No data logging or transmission to external servers
- You control model updates and versions

## 📊 Comparison: Local vs Cloud

| Feature | Local (Ollama) | Cloud (OpenAI) |
|---------|---------------|----------------|
| **Privacy** | ✅ Complete | ❌ Data sent to API |
| **Cost** | ✅ Free | ❌ Pay per token |
| **Speed** | ⚠️ Hardware dependent | ✅ Generally fast |
| **Quality** | ⚠️ Model dependent | ✅ High quality |
| **Offline** | ✅ Yes | ❌ Requires internet |
| **Customization** | ✅ Full control | ❌ Limited |

## 🛠 Advanced Configuration

### Custom Model Parameters

```json
{
    "NEUROSYMBOLIC_ENGINE_API_KEY": "ollama",
    "NEUROSYMBOLIC_ENGINE_MODEL": "your-custom-model",
    "NEUROSYMBOLIC_ENGINE_BASE_URL": "http://localhost:11434/v1",
    "NEUROSYMBOLIC_ENGINE_TEMPERATURE": 0.7,
    "NEUROSYMBOLIC_ENGINE_MAX_TOKENS": 2000,
    "NEUROSYMBOLIC_ENGINE_TOP_P": 0.9
}
```

### Multiple Models Setup

```bash
# Pull multiple models for different tasks
ollama pull deepseek-r1:14b      # Reasoning
ollama pull codellama:7b         # Coding
ollama pull llama3.2:3b          # Fast responses

# Switch between models in configuration as needed
```

### Custom Endpoints

```json
{
    "NEUROSYMBOLIC_ENGINE_BASE_URL": "http://your-server:11434/v1",
    "EMBEDDING_ENGINE_BASE_URL": "http://your-embedding-server:11434/v1"
}
```

## 📈 Performance Benchmarks

Approximate performance on different hardware:

| Hardware | Model | Tokens/sec | Response Time |
|----------|-------|------------|---------------|
| CPU (16 cores) | llama3.2:3b | 10-20 | 2-5s |
| CPU (16 cores) | deepseek-r1:14b | 3-8 | 5-15s |
| GPU (RTX 4090) | llama3.2:3b | 50-100 | 0.5-2s |
| GPU (RTX 4090) | deepseek-r1:14b | 20-40 | 2-8s |

## 🔗 Integration Examples

### Web Application
```python
from flask import Flask, request, jsonify
from symai import Symbol

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def query():
    text = request.json.get('text')
    question = request.json.get('question')
    
    symbol = Symbol(text)
    result = symbol.query(question)
    
    return jsonify({'result': str(result)})
```

### Batch Processing
```python
import pandas as pd
from symai import Symbol

# Process CSV data
df = pd.read_csv('data.csv')
results = []

for index, row in df.iterrows():
    symbol = Symbol(row['text'])
    result = symbol.query("Summarize this text")
    results.append(str(result))

df['summary'] = results
```

## 🎓 Learning Resources

- **SymbolicAI Documentation**: https://extensityai.gitbook.io/symbolicai
- **Ollama Documentation**: https://ollama.ai/docs
- **DeepSeek Models**: https://ollama.ai/library/deepseek-r1
- **Model Library**: https://ollama.ai/library

## 🤝 Contributing

To contribute to the Ollama integration:

1. Test with different models
2. Report performance benchmarks
3. Submit bug fixes and improvements
4. Share configuration optimizations

## 📄 License

This integration follows the same BSD-3-Clause License as SymbolicAI.

---

**🎉 Enjoy running SymbolicAI completely locally with full privacy and control!**