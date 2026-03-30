# Instructions for Advice QA Dataset Generation (RAG Eval - EUFARMBOOK)

Act as an expert in agriculture, forestry, biosecurity, and ecology. Analyze the attached PDF to generate situational advice question-and-answer (QA) pairs.

**IMPORTANT: The questions, answers, and JSON keys MUST strictly be in English. If the primary language of the document is NOT English, immediately return an empty array: `[]`**

## 1. Quantity & Style Requirements
- **Minimum output:** Generate a minimum of 5 questions per PDF.
- **Scenario-based questions:** Focus strictly on advice scenarios (e.g., "What should I do if...", "How can I prevent...", "What is the recommended approach for...").

## 2. Answer Requirements
- **Actionable & concrete:** Provide direct advice extracted exactly from the text.
- **Brevity:** Keep it as brief as possible. Do not output complete paragraphs or unnecessary explanations.

## 3. Contexts (Localization)
- Map the exact location of the advice.
- Extract the `page`, and the `section_name` if available. If no section name exists, use `null`.

## 4. Output Format
Output exclusively as a JSON array. Each question must have a sequentially incremental integer `id` starting from 0. 

```json
[
  {
    "id": 0,
    "question": "What should I do if [specific scenario] occurs?",
    "answer": "[Brief, actionable advice]",
    "contexts": [
      {
        "page": 1,
        "section_name": "[string or null]"
      }
    ]
  }
]