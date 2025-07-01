# SymbolicAI Playground

A comprehensive demonstration and playground for exploring [SymbolicAI](https://github.com/ExtensityAI/symbolicai) - a neuro-symbolic framework that combines classical Python programming with the differentiable, programmable nature of Large Language Models (LLMs). This playground supports both OpenAI's cloud models and local Ollama models.

## 🚀 Quick Start

Follow these steps to set up and run the demo with your preferred backend.

### 1. Choose and Set Up Your Backend

#### A. OpenAI Compatible (Cloud-Based)

1.  **Configure API Key**: Edit the `symai.config.openai.json` file in the root directory and add your OpenAI API key.

    ```json
    {
        "NEUROSYMBOLIC_ENGINE_API_KEY": "sk-your-actual-api-key-here",
        "NEUROSYMBOLIC_ENGINE_MODEL": "gpt-4o-mini",
        "EMBEDDING_ENGINE_API_KEY": "sk-your-actual-api-key-here",
        "EMBEDDING_ENGINE_MODEL": "text-embedding-3-small"
    }
    ```

2.  **Test the Setup**:
    ```bash
    ./symbolicai/bin/python test_engine.py openai-comp
    ```

#### B. Ollama (Local & Private)

1.  **Install Ollama**:
    ```bash
    # On Linux/macOS
    curl -fsSL https://ollama.ai/install.sh | sh
    ```
    For Windows, download from [ollama.ai](https://ollama.ai/).

2.  **Pull a Model**: You need at least one model to work with.
    ```bash
    # Recommended for reasoning
    ollama pull deepseek-r1:14b

    # Lightweight alternative for faster responses
    ollama pull llama3.2:3b
    ```

3.  **Start the Ollama Server**:
    ```bash
    ollama serve
    ```
    This command will run in the background.

4.  **Test the Setup**:
    ```bash
    ./symbolicai/bin/python test_engine.py ollama
    ```

### 2. Run the Unified Demo

Use the `main.py` script, specifying which backend configuration to use.

```bash
# Run with the OpenAI Compatible backend
./symbolicai/bin/python main.py openai-comp

# Run with the Ollama backend
./symbolicai/bin/python main.py ollama
```

## 🧪 Testing and Validation

For detailed instructions on how to test your setup and troubleshoot testing-related issues, please see the dedicated testing guide:

-   **[TESTING.md](TESTING.md)**

## 📁 Project Structure

```
symbolicai-playground/
├── src/
│   ├── demos/              # Demo scripts and modules
│   ├── engines/            # Backend engine integrations (OpenAI, Ollama)
│   ├── tests/              # Test implementations
│   └── utils/              # Utility modules
├── main.py                 # Main demo entry point
├── symai.config.openai.json# OpenAI configuration
├── symai.config.ollama.json# Ollama configuration
├── requirements.txt        # Package dependencies
├── README.md               # This file
└── TESTING.md              # Detailed testing documentation
```

## 🎭 What You'll Learn

The demo script (`main.py`) covers these key SymbolicAI concepts:

### 1. **Symbol Objects** - The Core Building Blocks
- **Syntactic Mode**: Behaves like normal Python values (default).
- **Semantic Mode**: Understands meaning and context via LLMs.
- **Projections**: Switch between modes with `.sem` and `.syn`.

```python
from symai import Symbol

# Syntactic (literal matching)
text = Symbol("Cats are adorable")
print("pets" in text)      # True (literal match)
print("feline" in text)  # False (no literal match)

# Semantic (meaning-based)
print("feline" in text.sem)  # True (understands meaning)
print("animals" in text.sem) # True (conceptual match)
```

### 2. **Primitives and Operations**
- Arithmetic: `+`, `-`, `*`, `/` with semantic meaning.
- Comparisons: `==`, `!=` with fuzzy/conceptual matching.
- Logical: `&`, `|` for inference and context merging.
- Transformations: `.map()`, `.filter()`, `.cluster()`.

### 3. **Contracts and Validation**
- Design by Contract principles for LLM reliability.
- Pre/post-condition validation and automatic remediation.
- Pydantic integration for structured data.

### 4. **Advanced Features**
- Data clustering and similarity analysis.
- Conditional processing with `.foreach()`.
- Choice selection from options.
- Vector embeddings and similarity metrics.

## ⚙️ Configuration

SymbolicAI supports multiple configuration methods, loaded in the following priority:

1.  **Local Directory**: `./symai.config.[backend].json` (used by this playground).
2.  **Environment Config**: `{python_env}/.symai/`.
3.  **Global Config**: `~/.symai/`.

### Cloud Configuration (`symai.config.openai.json`)
This file controls access to OpenAI and other cloud services.

```json
{
    "NEUROSYMBOLIC_ENGINE_API_KEY": "<API_KEY>",
    "NEUROSYMBOLIC_ENGINE_MODEL": "gpt-4o-mini",
    "SYMBOLIC_ENGINE_API_KEY": "<WOLFRAMALPHA_KEY>",
    "EMBEDDING_ENGINE_API_KEY": "<API_KEY>",
    "SEARCH_ENGINE_API_KEY": "<SERP_KEY>"
}
```

### Local Configuration (`symai.config.ollama.json`)
This file configures the connection to your local Ollama server.

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

Install optional features using `pip` from within the project's environment.

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

## 🐛 Troubleshooting

### OpenAI Issues
-   **API Key Error**: Make sure your OpenAI API key in `symai.config.openai.json` is valid and has sufficient credits.
-   **Connection Error**: Check your internet connection and that `https://api.openai.com` is reachable.
-   **Model Error**: Ensure you're using a model name available to your account (e.g., `gpt-4o-mini`, `gpt-4`).

### Ollama Issues
-   **Connection Error**: Ensure the Ollama server is running. Start it with `ollama serve`.
-   **Model Not Found**: Pull the required model via `ollama pull <model_name>` (e.g., `ollama pull deepseek-r1:14b`). You can see installed models with `ollama list`.
-   **Slow Performance**: Your hardware is the bottleneck. Try a lighter model for faster responses (e.g., `llama3.2:3b`) or consider running Ollama on a machine with a dedicated GPU.
-   **Out of Memory**: A large model is consuming too much RAM. Use a smaller model or increase your system's swap space.

## 🔗 Resources

-   **Documentation**: [https://extensityai.gitbook.io/symbolicai](https://extensityai.gitbook.io/symbolicai)
-   **GitHub**: [https://github.com/ExtensityAI/symbolicai](https://github.com/ExtensityAI/symbolicai)
-   **Research Paper**: [https://arxiv.org/abs/2402.00854](https://arxiv.org/abs/2402.00854)
-   **Ollama Models**: [https://ollama.ai/library](https://ollama.ai/library)
-   **Testing Guide**: [TESTING.md](TESTING.md)

## 📄 License

This playground is provided as-is for educational and experimental purposes. SymbolicAI itself is licensed under the BSD-3-Clause License.

---

**Happy Experimenting with Neuro-Symbolic AI! 🎉**