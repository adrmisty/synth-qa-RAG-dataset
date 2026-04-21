# Synthetic QA Dataset Generator (RAG Evaluation)

This pipeline generates and validates a synthetic silver standard Question-Answering dataset from PDF documents to evaluate Retrieval-Augmented Generation (RAG) systems, designed for the EUFARMBOOK domain.

The pipeline consists of two phases:
1. **Generation:** Uses the Gemini API to extract context-grounded QA pairs (both factual and advice-based) from English PDFs.
2. **Filtering:** Uses a local HuggingFace LLM (e.g., Qwen 2.5) to independently verify that the extracted contexts fully support the generated answers.

## Project Structure

* `main.py`: CLI entrypoint to execute the pipeline phases.
* `config.py`: Centralized configuration for model names, paths, and API keys.
* `generate.py`: Handles metadata integration, and Gemini API calls to generate the raw dataset.
* `filter.py`: Handles zero-shot validation using a local Hugging Face causal LM, outputting valid and invalid JSON datasets.
* `prompt.md` / `prompt_ADVICE.md`: System instructions for the Gemini generation phase in the `data/` directory.

## Requirements

Ensure you have a GPU-enabled environment for the local filtering phase.

```bash
pip install torch transformers pypdf tqdm langdetect accelerate google-genai
```

## Configuration

Before running, update your `config.py` with your paths, model preferences, and API key:

```python
API_KEY = "your_google_api_key"
GEN_MODEL_NAME = "gemini-2.0-flash" 
EVAL_MODEL_NAME = "Qwen/Qwen2.5-32B-Instruct" # or a smaller version if VRAM is limited
DOCS_DIR = "path/to/pdfs"
METADATA_DIR = "path/to/metadata"
```

## Usage

You can run the phases independently or together using command-line flags.

**Generate the raw dataset:**
```bash
python main.py --generate --min 100 --max 200
```

**Filter the dataset (Validation):**
```bash
python main.py --filter
```

**Run both sequentially:**
```bash
python main.py --generate --filter --min 50 --max 100
```

## Outputs

* `silver_dataset.json`: The raw output from the Gemini API.
* `filtered_silver_dataset.json`: The validated dataset containing only QA pairs where the context explicitly supports the answer.
* `filtered_silver_dataset.invalid.json`: Dropped QA pairs with the recorded `fail_reason` for debugging.
"""


## Author

**Adriana R. Flórez**
*Computational Linguist & Software Engineer*
[GitHub Profile](https://github.com/adrmisty) | [LinkedIn](https://linkedin.com/in/adriana-rodriguez-florez)

---

*Built with ❤️ using Python and HuggingFace.*
