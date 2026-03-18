# Instructions for silver standard dataset generation (RAG eval - EUFARMBOOK)

Act as an expert in agriculture, forestry, biosecurity, and ecology. Analyze the attached PDF to generate technical question-and-answer (QA) pairs.

**IMPORTANT:** 1. The questions and answers MUST be generated in English. 
2. The JSON keys must strictly remain in English. 
3. Generate a MINIMUM of 5 questions per PDF.

## 1. Question Requirements
- **Specificity:** Include technical terms, project names, or precise metrics that uniquely identify this document among thousands of others.
- **Self-Containment:** Do not use relative references (e.g., "in this document," "according to figure 2"). 

## 2. Answer Requirements
- **Brief but Specific:** Extract exclusively the hard data, numerical value, or specific technical term. Make it comprehensive but as brief as possible. 
- **No Paraphrasing:** Use the exact term as it appears in the text. [cite_start]DO NOT include citation tags (e.g., absolutely no "[cite: 123]").

## 3. Contexts (Localization)
- Map the exact location of the answer.
- Extract the `page`, and the `section_name` if available (use `null` if no section name exists).

## 4. Output Format
Output exclusively as a JSON array. Each question must have a sequentially incremental integer `id` starting from 0. Example based on a soil-based tomato production document:

```json
[
  {
    "id": 0,
    "question": "What is the suitable soil temperature range for Pyrenochaeta lycopersici to initiate an infection in tomatoes?",
    "answer": "Between 15 and 20°C",
    "contexts": [
      {
        "page": 1,
        "section_name": "Context"
      }
    ]
  },
  {
    "id": 1,
    "question": "How long do the microsclerotia of Pyrenochaeta lycopersici remain viable in the soil?",
    "answer": "10-15 years",
    "contexts": [
      {
        "page": 1,
        "section_name": "Context"
      }
    ]
  },
  {
    "id": 2,
    "question": "Which specific commercial mustard seed product was incorporated into the soil for the biofumigation treatment in the EcoStack methodology?",
    "answer": "Caliente mustard Brand 199",
    "contexts": [
      {
        "page": 2,
        "section_name": "Methodology and bioassay"
      }
    ]
  },
  {
    "id": 3,
    "question": "What specific tomato cultivar was used as the test plant to evaluate the effect of the biofumigation treatment?",
    "answer": "Solanum lycopersicum cv. Arvento",
    "contexts": [
      {
        "page": 2,
        "section_name": "Methodology and bioassay"
      }
    ]
  },
  {
    "id": 4,
    "question": "Which two soils showed a significant decrease in severe tomato root discoloration following biofumigation?",
    "answer": "Soils A and E",
    "contexts": [
      {
        "page": 3,
        "section_name": "Key findings"
      }
    ]
  }
]