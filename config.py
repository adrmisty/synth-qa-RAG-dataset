# config.py
# ----------------------------------------------------------
# configurations and paths
# ----------------------------------------------------------
# adriana r.f. (@adrmisty:github, arodriguezf@vicomtech.org)
# mar-2026

import os
from pathlib import Path

# gemini api key
API_KEY: str = os.getenv("GEMINI_ADRIANA_KEY")
GEN_MODEL_NAME = "gemini-3-flash-preview"
FILTER_MODEL_NAME = "Qwen/Qwen2.5-32B-Instruct"

# prompting and dataset
BASE_DATA_DIR: Path = Path("data")
PROMPT_DIR: Path = BASE_DATA_DIR / "prompt"

# dataset
DATASET_JSON: Path = BASE_DATA_DIR / "silver_dataset_QA.json"
FILTER_DATASET_JSON: Path = BASE_DATA_DIR / "filtered_silver_dataset_QA.json"

# prompts
PROMPT_MD: Path = PROMPT_DIR /  "prompt.md"
PROMPT_TXT: Path = PROMPT_DIR / "prompt.txt"
FILTER_PROMPT_TXT: str = (
    "You are an impartial evaluator. Given a context within a PDF document, a question, and an answer, "
    "verify if the context fully supports the answer to the question. "
    "Respond strictly with 'True' if the context supports the answer, or 'False' if it does not."
)


METADATA_DIR: Path = BASE_DATA_DIR / "ko" / "metadata"
DOCS_DIR: Path = BASE_DATA_DIR / "ko" / "pdf"