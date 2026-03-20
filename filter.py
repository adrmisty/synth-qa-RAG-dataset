# filter.py
# ----------------------------------------------------------------------------------------
# filtering on Qwen for silver standard dataset
# asking a smaller model to validate answer for a question for a given context
# ----------------------------------------------------------------------------------------
# adriana r.f. (@adrmisty:github, arodriguezf@vicomtech.org)
# mar-2026

import json
import torch
import logging
from pypdf import PdfReader
from pathlib import Path
from tqdm import tqdm
import config
from transformers import AutoModelForCausalLM, AutoTokenizer

logging.basicConfig(level=logging.INFO, format="INFO: %(message)s")

class SilverDatasetFilter:
    def __init__(self, model_id: str, docs_dir: Path = config.DOCS_DIR):
        """
        Inits the Qwen evaluator for QA pair validation.
        """
        self.model_id = model_id
        self.docs_dir = Path(docs_dir)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()

    # --- filtering logic -------------------------------------------------------------------------

    def filter_dataset(self, prompt: str, input_json: str, output_json: str):
        with open(input_json, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        filtered_dataset = []
        invalid_dataset = []
        
        logging.info("> Starting QA validation and filtering...")
        for doc in tqdm(dataset):
            doc_id = doc["document_id"]
            pdf_path = self.docs_dir / f"{doc_id}.pdf"
            
            if not pdf_path.exists():
                continue

            valid_qa_pairs = []
            invalid_qa_pairs = []
            
            for qa in doc["qa_pairs"]:
                # context extraction
                page_num = qa["contexts"]["page"] 
                context_text = self._extract_page_text(pdf_path, page_num)
                
                if not context_text:
                    continue

                user_prompt = (
                    f"Context:\n{context_text}\n\n"
                    f"Question: {qa['question']}\n"
                    f"Answer: {qa['answer']}"
                )
                
                decision = self._generate(prompt, user_prompt)
                
                # only retrieve the validated ones
                if "True" in decision:
                    valid_qa_pairs.append(qa)
                else:
                    invalid_qa_pairs.append(qa)
                    
            if valid_qa_pairs:
                doc["qa_pairs"] = valid_qa_pairs
                filtered_dataset.append(doc)
            if invalid_qa_pairs:
                doc["qa_pairs_invalid"] = invalid_qa_pairs
                invalid_dataset.append(doc)
                
        # ** dump both valid and invalid QA pairs **
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(filtered_dataset, f, ensure_ascii=False, indent=4)
        with open(output_json.with_suffix(".invalid.json"), "w", encoding="utf-8") as f:
            json.dump(invalid_dataset, f, ensure_ascii=False, indent=4)
            
        logging.info(f">>> Filtering complete, results saved to {output_json}!")


    # --- model init -------------------------------------------------------------------------

    def _load_model(self):
        """Loads a smaller Qwen model that wil be used for zero-shot evaluation and filtering of the generated dataset."""
        logging.info(f"> Loading {self.model_id} on {self.device} for evaluation...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
        )
        self.model.eval()
        logging.info(f"\t >>> {self.model_id} model loaded successfully!")

    def _generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generates response from Qwen model for the given system and user prompts, and extracts the True/False decision
        for a given QA pair in a specific context."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                model_inputs.input_ids,
                max_new_tokens=10,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True).strip().upper()

    # --- dataset processing -----------------------------------------------------------------

    def _extract_page_text(self, pdf_path: Path, page_num: int) -> str:
        """For a context within a PDF document, extract the text from the specified page number."""
        try:
            reader = PdfReader(pdf_path)
            # PDF pages are 0-indexed in pypdf; assuming JSON is 1-indexed
            page_index = page_num - 1
            
            if 0 <= page_index < len(reader.pages):
                page = reader.pages[page_index]
                text = page.extract_text()
                return text.strip() if text else ""
            else:
                logging.warning(f"Page {page_num} is out of bounds for {pdf_path.name}")
                return ""
        except Exception as e:
            logging.error(f"Error reading {pdf_path.name} page {page_num}: {e}")
            return ""