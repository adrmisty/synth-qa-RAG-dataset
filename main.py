# main.py
# --------------------------------------------------------------------------------------------------------------
# entrypoint for silver standard dataset generation 
# ---------------------------------------------------------------------------------------------------------------
# adriana r.f. (@adrmisty:github, arodriguezf@vicomtech.org)
# mar-2026

import argparse
import random
import config
from silver_data import SilverDatasetGenerator

def main():
    parser = argparse.ArgumentParser(description="Synthetic silver standard QA dataset generation for RAG evaluation")
    parser.add_argument("--min", help="Minimum number of documents to sample", type=int, default=100)
    parser.add_argument("--max", help="Maximum number of documents to sample", type=int, default=200)
    
    args = parser.parse_args()

    generator = SilverDatasetGenerator(
        api_key=config.API_KEY, 
        metadata_dir=config.METADATA_DIR, 
        docs_dir=config.DOCS_DIR,
        prompt_path=config.PROMPT_MD,
        model_name=config.MODEL_NAME
    )
    
    sample_size = random.randint(args.min, args.max)
    generator.generate_QA_sample(sample_size=sample_size)
    
if __name__ == "__main__":
    main()