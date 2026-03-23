# main.py
# -----------------------------------------------------------------
# silver standard dataset generation and filtering for EUFARMBOOK
# -----------------------------------------------------------------
# adriana r.f. (@adrmisty:github, arodriguezf@vicomtech.org)
# mar-2026

import argparse
import random
import config
from generate import SilverDatasetGenerator  
from filter import SilverDatasetFilter, get_filter_stats

def main():
    parser = argparse.ArgumentParser(description="Synthetic silver standard QA dataset for RAG evaluation")
    
    parser.add_argument("--generate", action="store_true", help="Run the dataset generation phase using Gemini")
    parser.add_argument("--filter", action="store_true", help="Run the dataset filtering phase using Qwen")
    parser.add_argument("--stats", action="store_true", help="(Aux) Computes statistics for the filtered dataset")

    parser.add_argument("--min", help="Minimum number of documents to sample", type=int, default=100)
    parser.add_argument("--max", help="Maximum number of documents to sample", type=int, default=200)

    args = parser.parse_args()

    if args.generate:
        print("\n--- SILVER EUFB DATASET (1): GENERATION ---")
        generator = SilverDatasetGenerator(
            api_key=config.API_KEY, 
            metadata_dir=config.METADATA_DIR, 
            docs_dir=config.DOCS_DIR,
            prompt_path=config.PROMPT_MD,
            model_name=config.GEN_MODEL_NAME # Make sure this is in config.py
        )
        sample_size = random.randint(args.min, args.max)
        generator.generate_QA_sample(sample_size=sample_size, output_file=config.DATASET_JSON)
        
    if args.filter:
        print("\n--- SILVER EUFB DATASET (2): FILTERING ---")
        evaluator = SilverDatasetFilter(
            model_id=config.FILTER_MODEL_NAME,
            docs_dir=config.DOCS_DIR
        )
        evaluator.filter_dataset(
            prompt=config.FILTER_PROMPT_TXT,
            input_json=config.DATASET_JSON,
            output_json=config.FILTER_DATASET_JSON
        )
    
    if args.stats: # post-filtering statistics
        get_filter_stats(filepath=config.FILTER_DATASET_JSON, invalid=False)
        get_filter_stats(filepath=config.FILTER_DATASET_JSON, invalid=True)

if __name__ == "__main__":
    main()