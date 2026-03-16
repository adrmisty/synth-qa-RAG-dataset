# Instructions for silver standard dataset generation (RAG eval - EUFARMBOOK)

Act as an expert in agriculture, forestry, biosecurity, and ecology. Analyze the attached PDF to generate technical question-and-answer (QA) pairs.

**IMPORTANT: The questions and answers must be generated in the original language of the PDF text (e.g., Spanish, Greek, Italian). The JSON keys must strictly remain in English.**

## 1. Question Requirements
- **Specificity:** Include technical terms, project names, or precise metrics that uniquely identify this document among thousands of others.
- **Self-Containment:** Do not use relative references (e.g., "in this document," "according to figure 2"). 

## 2. Answer Requirements
- **Brief but Specific:** Extract exclusively the hard data, numerical value, or specific technical term. Make it comprehensive but as brief as possible. 
- **No Paraphrasing:** Use the exact term as it appears in the text.

## 3. Contexts (Localization)
- Map the exact location of the answer.
- Extract the `page`, the `section` identifier (if available), and the `section_name`.

## 4. Output Format
Output exclusively as a JSON array (example document: 'DISEASE CONTROL IN SOIL-BASED TOMATOPRODUCTION'):

```json
[
  {
    "question": "What is the suitable soil temperature range for Pyrenochaeta lycopersici to initiate an infection in tomatoes? [cite: 240]",
    "answer": "Between 15 and 20°C [cite: 240]",
    "contexts": [
      {
        "page": 1,
        "section": null,
        "section_name": "Context"
      }
    ]
  },
  {
    "question": "How long do the microsclerotia of Pyrenochaeta lycopersici remain viable in the soil? [cite: 242]",
    "answer": "10-15 years [cite: 242]",
    "contexts": [
      {
        "page": 1,
        "section": null,
        "section_name": "Context"
      }
    ]
  },
  {
    "question": "Which specific commercial mustard seed product was incorporated into the soil for the biofumigation treatment in the EcoStack methodology? [cite: 256]",
    "answer": "Caliente mustard Brand 199 [cite: 256]",
    "contexts": [
      {
        "page": 2,
        "section": null,
        "section_name": "Methodology and bioassay"
      }
    ]
  },
  {
    "question": "What specific tomato cultivar was used as the test plant to evaluate the effect of the biofumigation treatment? [cite: 258]",
    "answer": "Solanum lycopersicum cv. Arvento [cite: 258]",
    "contexts": [
      {
        "page": 2,
        "section": null,
        "section_name": "Methodology and bioassay"
      }
    ]
  }
]