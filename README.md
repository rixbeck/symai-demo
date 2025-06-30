# SymbolicAI Playground

A comprehensive demonstration and playground for exploring [SymbolicAI](https://github.com/ExtensityAI/symbolicai) - a neuro-symbolic framework that combines classical Python programming with the differentiable, programmable nature of Large Language Models (LLMs). Now supports both OpenAI's cloud models and local Ollama models!

## 🚀 Quick Start

### Option A: Using OpenAI (Cloud-Based)

1. Edit `symai.config.json` and replace `<YOUR_OPENAI_API_KEY>` with your actual OpenAI API key:

```json
{
    "NEUROSYMBOLIC_ENGINE_API_KEY": "sk-your-actual-api-key-here",
    "NEUROSYMBOLIC_ENGINE_MODEL": "gpt-4o-mini",
    "EMBEDDING_ENGINE_API_KEY": "sk-your-actual-api-key-here",
    "EMBEDDING_ENGINE_MODEL": "text-embedding-3-small",
    "SUPPORT_COMMUNITY": false
}
```

2. Run the demo:
```bash
./symbolicai/bin/python main.py
```

### Option B: Using Ollama (Local & Private)

1. Install Ollama:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

2. Pull a model:
```bash
ollama pull deepseek-r1:14b  # or llama3.2:3b for lighter usage
```

3. Start Ollama:
```bash
ollama serve
```

4. Run the Ollama demo:
```bash
./symbolicai/bin/python main_ollama.py
```

See [README_OLLAMA.md](README_OLLAMA.md) for detailed local setup instructions.

## 📁 Project Structure

```
symbolicai-playground/
├── symbolicai/                # Conda environment with Python 3.11.13
├── main.py                   # OpenAI demo script
├── main_ollama.py           # Ollama demo script
├── ollama_engine.py         # Custom Ollama integration
├── symai.config.json        # OpenAI configuration
├── symai.config.ollama.json # Ollama configuration
├── requirements.txt         # Package dependencies
├── README.md               # This file
└── README_OLLAMA.md        # Ollama setup guide
```

## 🎭 What You'll Learn

The demo script (`main.py`) covers these key SymbolicAI concepts:

### 1. **Symbol Objects** - The Core Building Blocks
- **Syntactic Mode**: Behaves like normal Python values (default)
- **Semantic Mode**: Understands meaning and context via LLMs
- **Projections**: Switch between modes with `.sem` and `.syn`

```python
from symai import Symbol

# Syntactic (literal matching)
text = Symbol("Cats are adorable")
print("pets" in text)  # True (literal match)
print("feline" in text)  # False (no literal match)

# Semantic (meaning-based)
print("feline" in text.sem)  # True (understands meaning)
print("animals" in text.sem)  # True (conceptual match)
```

### 2. **Primitives and Operations**
- Arithmetic: `+`, `-`, `*`, `/` with semantic meaning
- Comparisons: `==`, `!=` with fuzzy/conceptual matching
- Logical: `&`, `|` for inference and context merging
- Transformations: `.map()`, `.filter()`, `.cluster()`

### 3. **Contracts and Validation**
- Design by Contract principles for LLM reliability
- Pre/post-condition validation
- Automatic remediation and retry logic
- Pydantic integration for structured data

### 4. **Advanced Features**
- Data clustering and similarity analysis
- Conditional processing with `.foreach()`
- Choice selection from options
- Vector embeddings and similarity metrics

## 🔧 Configuration Options

SymbolicAI supports multiple configuration methods (in priority order):

1. **Debug Mode**: `./symai.config.json` or `./symai.config.ollama.json` (current directory)
2. **Environment Config**: `{python_env}/.symai/`
3. **Global Config**: `~/.symai/`

### Cloud Configuration (OpenAI)

```json
{
    "NEUROSYMBOLIC_ENGINE_API_KEY": "<API_KEY>",
    "NEUROSYMBOLIC_ENGINE_MODEL": "gpt-4o-mini",
    "SYMBOLIC_ENGINE_API_KEY": "<WOLFRAMALPHA_KEY>",
    "EMBEDDING_ENGINE_API_KEY": "<API_KEY>",
    "SEARCH_ENGINE_API_KEY": "<SERP_KEY>",
    "TEXT_TO_SPEECH_ENGINE_API_KEY": "<API_KEY>",
    "DRAWING_ENGINE_API_KEY": "<API_KEY>",
    "OCR_ENGINE_API_KEY": "<APILAYER_KEY>",
    "INDEXING_ENGINE_API_KEY": "<PINECONE_KEY>"
}
```

### Local Configuration (Ollama)

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

## 📦 Installing Additional Features

```bash
# Web search capabilities
./symbolicai/bin/pip install "symbolicai[serpapi]"

# Speech processing (requires ffmpeg)
./symbolicai/bin/pip install "symbolicai[whisper]"

# Web crawling
./symbolicai/bin/pip install "symbolicai[selenium]"

# Symbolic computation
./symbolicai/bin/pip install "symbolicai[wolframalpha]"

# Vector databases
./symbolicai/bin/pip install "symbolicai[pinecone]"

# Everything at once
./symbolicai/bin/pip install "symbolicai[all]"
```

## 🎯 Example Use Cases

### Text Analysis and Transformation
```python
from symai import Symbol

# Semantic text processing
reviews = Symbol([
    "This product is amazing!",
    "Terrible quality, waste of money",
    "Pretty good, would recommend"
])

# Classify sentiment
sentiments = reviews.map("classify sentiment as positive/negative/neutral")
```

### Data Clustering
```python
# Cluster related items semantically
cities = Symbol([
    "Paris", "London", "Tokyo", "New York", 
    "Rome", "Berlin", "Sydney", "Toronto"
])

clusters = cities.cluster()  # Groups by geographic/cultural similarity
```

### Contract-Based Validation
```python
from symai import Expression
from symai.strategy import contract

@contract(pre_remedy=True, post_remedy=True)
class DataExtractor(Expression):
    prompt = "Extract structured information from text"
    
    def forward(self, text, **kwargs):
        # LLM processing with automatic validation
        return validated_data
```

## 🔗 Resources

- **Documentation**: [https://extensityai.gitbook.io/symbolicai](https://extensityai.gitbook.io/symbolicai)
- **GitHub**: [https://github.com/ExtensityAI/symbolicai](https://github.com/ExtensityAI/symbolicai)
- **Research Paper**: [https://arxiv.org/abs/2402.00854](https://arxiv.org/abs/2402.00854)
- **DeepWiki**: [https://deepwiki.com/ExtensityAI/symbolicai](https://deepwiki.com/ExtensityAI/symbolicai)
- **Examples**: [https://github.com/ExtensityAI/symbolicai/tree/main/examples](https://github.com/ExtensityAI/symbolicai/tree/main/examples)
- **Ollama Guide**: [README_OLLAMA.md](README_OLLAMA.md) - Detailed local setup instructions
- **Ollama Models**: [https://ollama.ai/library](https://ollama.ai/library)

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI Issues**:
   - API Key Error: Make sure your OpenAI API key is valid and has sufficient credits
   - Connection Error: Check your internet connection and API endpoints
   - Model Error: Ensure you're using a supported model (gpt-4o-mini, gpt-4, etc.)

2. **Ollama Issues**:
   - Connection Error: Ensure Ollama is running (`ollama serve`)
   - Model Not Found: Pull the required model (`ollama pull deepseek-r1:14b`)
   - Performance: Try a lighter model for faster responses (`llama3.2:3b`)

3. **General Issues**:
   - Import Error: Verify SymbolicAI is installed: `./symbolicai/bin/pip list | grep symbolic`

### Getting Help

```bash
# Check current configuration
./symbolicai/bin/python -c "import symai; print(symai.__version__)"

# Run tests
./symbolicai/bin/python -m pytest tests/

# View configuration
./symbolicai/bin/symconfig
```

## 🚀 Next Steps

1. **Experiment**: Modify `main.py` to try your own examples
2. **Explore**: Check out the official documentation and examples
3. **Build**: Create your own neuro-symbolic applications
4. **Contribute**: Join the SymbolicAI community and contribute to the project

## 📄 License

This playground is provided as-is for educational and experimental purposes. 
SymbolicAI itself is licensed under BSD-3-Clause License.

---

**Happy Experimenting with Neuro-Symbolic AI! 🎉**