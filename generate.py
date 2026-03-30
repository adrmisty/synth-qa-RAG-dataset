# generate.py
# ----------------------------------------------------------------------------------------
# silver standard QA dataset generation for RAG evaluation using Gemini
# ----------------------------------------------------------------------------------------
# adriana r.f. (@adrmisty:github, arodriguezf@vicomtech.org)
# mar-2026

import json
import random
import logging
from pathlib import Path
from tqdm import tqdm
from google import genai
from google.genai import types
from langdetect import detect
from pypdf import PdfReader

logging.basicConfig(level=logging.INFO, format="INFO: %(message)s")

class SilverDatasetGenerator:
    def __init__(self, api_key: str, metadata_dir: Path, docs_dir: Path, prompt_path: Path, model_name: str):
        """
        Inits the generator for RAG evaluation datasets.
        """
        self.client = genai.Client(api_key=api_key)
        self.metadata_dir = metadata_dir
        self.docs_dir = docs_dir
        self.model_name = model_name
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_instruction = f.read()

    # --- generation logic -------------------------------------------------------------------

    def generate_QA_sample(self, sample_size: int, output_file: str = "data/silver_dataset_QA.json"):
        """Generates QA pairs for evaluation of a RAG system."""
        valid_docs = []
        
        # extract all metadata
        for meta_file in self.metadata_dir.glob("*.json"):
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta_content = json.load(f)
                    if meta_content.get("valid_structure"):
                        valid_docs.append(meta_file.stem)
            except Exception:
                continue

        sampled_ids = random.sample(valid_docs, min(sample_size, len(valid_docs)))
        dataset = []
        logging.info(f"> Starting [silver-standard synthetic QA dataset] generation for {len(sampled_ids)} documents...")

        for doc_id in tqdm(sampled_ids):
            pdf_path = self.docs_dir / f"{doc_id}"
            meta_path = self.metadata_dir / f"{doc_id}.json"
            
            if not pdf_path.exists():
                logging.warning(f"\t> (!) File not found: {pdf_path}")
                continue

            """ ** langdetect not so good **
            if not self._is_english(pdf_path):
                logging.info(f"\t> (!) File not in English: {pdf_path}")
                continue
            """ 
            try:
                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()
                    
                with open(meta_path, "r", encoding="utf-8") as f:
                    doc_metadata = json.load(f)

                # ** dynamic topic, theme and keywords ** > inject in prompt
                topic = doc_metadata.get("topic", "N/A")
                theme = doc_metadata.get("theme", "N/A")
                keywords = ", ".join(doc_metadata.get("keywords", []))
                context_injection = (
                    f"Additional document context:\n"
                    f"- Topic: {topic}\n"
                    f"- Theme: {theme}\n"
                    f"- Keywords: {keywords}\n\n"
                    f"Generate the JSON strictly matching the requested format."
                )

                # get GEMINI response in the required .json format
                response = self.client.models.generate_content(
                    model=self.model_name,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        response_mime_type="application/json",
                    ),
                    contents=[
                        types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                        context_injection
                    ],
                )

                qa_content = json.loads(response.text)
                if not qa_content:
                    continue
                
                dataset.append({
                    "document_id": doc_id, # metadata-extracted
                    "category": topic,     # metadata-extracted [required action point]
                    #"metadata": doc_metadata, do not include metadata for now, only the QA pairs
                    "qa_pairs": qa_content
                })

            except Exception as e:
                logging.error(f"\t (!) > Error processing {doc_id}: {e}")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
        
        logging.info(f">>> QA dataset saved to {output_file}!")

    # --- english filter-out -------------------------------------------------------------------

    def _is_english(self, pdf_path: Path) -> bool:
            """Ensures the document is English before making API calls."""
            try:
                reader = PdfReader(pdf_path)
                if reader.pages:
                    text = reader.pages.extract_text()
                    if text and detect(text) == 'en':
                        return True
            except Exception:
                pass
            return False