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
MODEL_NAME = "gemini-3-flash-preview"

# prompting and dataset
BASE_DATA_DIR: Path = Path("data")
PROMPT_MD: Path = BASE_DATA_DIR / "prompt.md"
PROMPT_TXT: Path = BASE_DATA_DIR / "prompt.txt"

DATASET_JSON: Path = BASE_DATA_DIR / "silver_dataset_QA.json"

METADATA_DIR: Path = BASE_DATA_DIR / "ko" / "metadata"
DOCS_DIR: Path = BASE_DATA_DIR / "ko" / "pdf"