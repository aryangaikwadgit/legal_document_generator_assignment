# Legal Document Generation & Evaluation Agent

A GenAI-powered system for generating and evaluating an **Affidavit in Reply** from case information while preserving the structure and drafting conventions of reference legal documents.

## Live Demo

**Streamlit App:** https://legal-document-generator.streamlit.app/

---

## 1. Project Objective

The objective is to build a reusable legal-document generation pipeline that can:

1. Understand a legal document format.
2. Analyze a sample document to learn presentation and drafting structure.
3. Extract structured case information from a case PDF.
4. Map extracted information to the learned document structure.
5. Generate an Affidavit in Reply using an LLM.
6. Build DOCX and PDF outputs.
7. Validate the generated document using deterministic rules.
8. Evaluate the document across multiple quality dimensions.
9. Generate an evaluation report.
10. Track LLM token usage.

The system is specifically scoped to **Affidavit in Reply** generation. It does not perform legal research or autonomous legal reasoning.

---

## 2. Input Documents

The pipeline uses three documents:

### `01_Affidavit_Format_Explained.pdf`

Defines the expected legal-document format, required sections, fixed conventions, and structural requirements.

### `02_Affidavit_in_Reply_Sample.pdf`

A completed sample Affidavit in Reply used as a reference for section order, headings, party presentation, paragraph numbering, prayer formatting, jurat, verification, advocate block, and general presentation.

Case-specific facts from the sample are not copied into the generated document.

### `03_Case_Information.pdf`

Contains the actual case-specific information used for generation, including court and jurisdiction, case details, parties, answering respondent, deponent, exhibits, reply points, prayer points, verification information, and advocate details.

---

## 3. High-Level Workflow

```text
Reference Documents
        |
        v
Template Analysis
        |
        v
Case Information PDF
        |
        v
Text Extraction + Chunking
        |
        v
Structured Entity Extraction
        |
        v
Content Mapping
        |
        v
LLM Document Generation
        |
        v
DOCX / PDF Generation
        |
        v
Deterministic Validation
        |
        v
Evaluation
        |
        v
Evaluation Report
```

The core design separates:

**WHAT the document should say**  
→ structured case information

**HOW the document should be presented**  
→ learned document structure

---

## 4. Architecture

```text
Streamlit UI
    |
    v
LegalDocumentGenerator
    |
    +--> PDFParser
    +--> TextChunker
    +--> CaseExtractor --------> CaseInformation
    +--> TemplateAnalyzer -----> DocumentStructure
    +--> ContentMapper
    +--> AffidavitGenerator ---> GeneratedDocument
    +--> DocumentBuilder ------> DOCX
    +--> PDFBuilder -----------> PDF
    +--> AffidavitValidator
    +--> AffidavitEvaluator
    +--> EvaluationReportGenerator
    +--> TokenTracker
```

---

## 5. Technology Stack

- Python
- Streamlit
- FastAPI
- LangChain
- Ollama
- Pydantic
- PyMuPDF (`fitz`)
- python-docx
- ReportLab
- python-dotenv

LangChain is used for LLM orchestration and structured output parsing. Pydantic provides structured contracts for extraction and generation.

---

## 6. Project Structure

```text
legal_document_generator_assignment/
│
├── backend/
│   ├── src/
│   │   ├── parser.py
│   │   ├── chunker.py
│   │   ├── extractor.py
│   │   ├── template_analyzer.py
│   │   ├── mapper.py
│   │   ├── generator.py
│   │   ├── schemas.py
│   │   ├── prompts.py
│   │   ├── document_builder.py
│   │   ├── pdf_builder.py
│   │   ├── validators.py
│   │   ├── evaluator.py
│   │   ├── report_generator.py
│   │   ├── token_tracker.py
│   │   └── config.py
│   │
│   ├── pipeline.py
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── data/
│   └── reference/
│       ├── 01_Affidavit_Format_Explained.pdf
│       └── 02_Affidavit_in_Reply_Sample.pdf
│
├── outputs/
├── .env
├── .gitignore
└── README.md
```

---

## 7. Structured Data Design

Pydantic models are used to keep LLM output structured and predictable.

### `CaseInformation`

Stores:

- forum
- jurisdiction
- case type
- case number and year
- petitioner
- respondents
- answering respondent
- deponent
- verification information
- exhibits
- place and date
- advocate firm
- reply points
- prayer points

### `DocumentStructure`

Represents the structure learned from the reference documents.

Each section can contain:

- section name
- order
- placeholder
- instruction
- numbering
- alignment
- formatting

### `GeneratedDocument`

Represents the generated affidavit as structured sections:

- heading
- cause title
- affidavit title
- deponent
- numbered paragraph
- prayer heading
- prayer intro
- prayer item
- jurat
- verification
- advocate

The structured representation is then converted into DOCX and PDF.

---

## 8. Template Understanding

The system does not simply copy the sample document.

The two reference documents have separate responsibilities.

### Format document

Used to determine:

- required sections
- legal-document requirements
- fixed conventions
- numbering
- structural rules

### Sample document

Used to learn:

- section order
- presentation
- alignment
- headings
- spacing
- prayer layout
- jurat
- verification
- advocate block

This produces a reusable template representation instead of hard-coding the entire sample affidavit.

---

## 9. LLM Extraction

The `CaseExtractor` sends the case information text to the LLM and requests output matching the `CaseInformation` Pydantic schema.

Important extraction rules include:

- extract only explicitly stated information
- do not invent facts
- preserve names and numbers
- preserve respondent numbering
- preserve exhibit information
- keep reply points in their original order
- combine bullets belonging to the same parent-level reply point
- ignore unrelated content

The result is parsed using LangChain's `PydanticOutputParser`.

---

## 10. Content Mapping

The `ContentMapper` connects extracted case information with the learned document structure.

```text
Case Information = WHAT
Template Structure = HOW
```

The mapped content is passed to the generation stage.

---

## 11. Controlled Document Generation

The `AffidavitGenerator` uses the LLM to generate a structured `GeneratedDocument`.

Generation rules include:

- use only supplied case information
- follow the learned section order
- do not copy sample-specific parties or facts
- do not invent facts or reliefs
- preserve respondent numbering
- generate exactly one body paragraph for each supplied reply point
- add the required closing paragraph
- generate prayer items from supplied prayer points
- use the actual verification paragraph range
- use supplied deponent, date, place, and advocate information

If a required case-specific value is missing:

```text
[NOT PROVIDED]
```

is used instead of guessing.

---

## 12. Paragraph Handling

A key requirement is the distinction between reply points and the mandatory closing paragraph.

For example:

```text
6 reply points
+
1 mandatory closing paragraph
=
7 numbered body paragraphs
```

The verification section must therefore refer to the actual generated range, rather than copying the paragraph range from the sample.

---

## 13. Document Generation

### DOCX

Generated using `python-docx`.

The document uses legal-document-oriented formatting including:

- US Letter page size
- controlled margins
- fixed table layout where required
- centered `VERSUS`
- structured cause title
- numbered paragraphs
- prayer formatting
- jurat and verification
- advocate block

### PDF

Generated separately using ReportLab.

The final layout places the **PRAYER section on the next page** to match the required presentation.

Outputs:

```text
affidavit_in_reply.docx
affidavit_in_reply.pdf
```

---

## 14. Validation

Validation is primarily deterministic rather than relying on the LLM to judge its own output.

### Entity Accuracy

Checks important case entities such as:

- forum
- case details
- petitioner
- respondents
- answering respondent
- deponent
- advocate
- dates
- place

### Completeness

Checks required sections and required information.

### Structure

Checks:

- required sections
- section order
- paragraph numbering
- prayer structure
- verification
- jurat

### Consistency

Checks relationships such as:

- respondent number consistency
- answering respondent consistency
- verification paragraph range
- dates and place
- exhibit references

### Hallucination Guard

Checks whether generated content introduces information that was not supplied in the case information.

---

## 15. Evaluation

The `AffidavitEvaluator` calculates scores across:

```text
Entity Accuracy
Completeness
Structure
Consistency
Template Fidelity
Hallucination
```

The evaluation produces an overall score as well as dimension-level results.

This allows the system to distinguish between:

```text
"the document was generated"
```

and:

```text
"the generated document satisfies measurable quality requirements."
```

---

## 16. Evaluation Report

The `EvaluationReportGenerator` creates:

```text
evaluation_report.json
```

The report contains the evaluation results and provides a machine-readable summary of document quality.

---

## 17. Token Tracking

LLM usage is tracked through the `TokenTracker`.

The system records:

```text
input_tokens
output_tokens
total_tokens
```

This provides visibility into LLM consumption across the extraction, template analysis, and generation stages.

---

## 18. Why No Vector Database / RAG?

A vector database was intentionally not introduced because the assignment only requires understanding two reference documents and one case document.

The references are supplied directly to the template-analysis stage:

```text
reference documents
        ↓
template analysis
        ↓
structured reusable document structure
```

This avoids unnecessary retrieval infrastructure while keeping the solution aligned with the assignment.

---

## 19. Why Deterministic Validation?

LLMs are useful for semantic understanding and drafting, but exact requirements are better checked with deterministic rules.

Therefore, Python validation is used for requirements such as:

- exact respondent numbers
- paragraph counts
- verification ranges
- required sections
- prayer lettering
- exhibit references
- consistency
- hallucination checks

The resulting approach is:

```text
LLM
→ semantic understanding and generation

Python
→ orchestration, validation and scoring

Pydantic
→ structured data contracts
```

---

## 20. Error Handling Philosophy

The system prefers visible failures over silent assumptions.

Examples:

```text
Missing information
→ [NOT PROVIDED]

Invalid structured LLM output
→ parser/validation failure

Wrong respondent number
→ validation issue

Wrong paragraph range
→ validation issue

Unexpected generated information
→ hallucination validation issue
```

---

## 21. Installation

Clone the repository:

```bash
git clone https://github.com/aryangaikwadgit/legal_document_generator_assignment.git
cd legal_document_generator_assignment
```

Create a virtual environment.

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

---

## 22. Environment Variables

Create a `.env` file in the project root.

### Sample `.env`

```env
OLLAMA_API_KEY=your_ollama_api_key_here
OLLAMA_MODEL=gpt-oss:120b-cloud
```

Replace the placeholder with your own Ollama API key.

**Never commit the real `.env` file or API key to GitHub.**

A safe repository example can be:

```text
.env.example
```

with placeholder values only.

---

## 23. Streamlit Secrets

For Streamlit Cloud deployment, configure the same values in the application's Secrets settings.

Example:

```toml
OLLAMA_API_KEY = "your_ollama_api_key_here"
OLLAMA_MODEL = "gpt-oss:120b-cloud"
```

Never expose the real API key in source code, screenshots, README files, commits, or public repositories.

---

## 24. Running Locally

From the project root:

```bash
streamlit run frontend/app.py
```

Then:

1. Upload the Case Information PDF.
2. Click **Generate Document**.
3. Wait for extraction, template analysis, generation, validation, and evaluation.
4. Download the generated PDF, DOCX, and evaluation report.

---

## 25. Running the API

The project also contains a FastAPI layer.

From the backend directory:

```bash
cd backend
uvicorn api:app --reload
```

The API exposes:

```text
POST /generate
```

It accepts the Case Information PDF and returns generated-document information, validation results, evaluation results, and file references.

---

## 26. Output

The pipeline produces:

```text
outputs/
├── uploaded_case_information.pdf
├── affidavit_in_reply.docx
├── affidavit_in_reply.pdf
└── evaluation_report.json
```

---

## 27. Important Design Decisions

### Structured LLM output

Pydantic schemas are used instead of relying on free-form model responses.

### Separate extraction and generation

The model first extracts structured information and only then generates the document.

### Separate template learning

Template analysis is performed independently from case extraction.

### Sample facts are isolated

The sample affidavit is used for style and structure, not as a source of case facts.

### Deterministic evaluation

Exact requirements are checked using Python rules.

### No unnecessary retrieval infrastructure

No vector database is required for the supplied reference documents.

### Token tracking

LLM usage is measured for transparency and cost awareness.

### Reusable document schema

The generated document is represented as structured sections before formatting.

---

## 28. Limitations

This system is intentionally scoped.

It does not:

- perform legal research
- provide legal advice
- independently determine legal strategy
- perform para-wise petition replies
- verify legal authorities
- replace review by a qualified legal professional
- guarantee that generated legal content is legally sufficient

The system demonstrates document generation and evaluation methodology rather than autonomous legal practice.

---

## 29. Future Improvements

Potential extensions include:

- support for additional legal document types
- stronger evidence-to-paragraph mapping
- richer validation rules
- human-in-the-loop review
- versioned templates
- improved document layout controls
- detailed evaluation dashboards
- configurable generation policies
- additional document-level quality metrics

These are outside the minimum implementation scope.

---

## 30. Security Notes

The application uses an external LLM service.

Therefore:

- API keys must be stored as environment variables or deployment secrets.
- Secrets must never be committed to Git.
- Case documents may contain sensitive legal information.
- Production use should apply appropriate data-protection, access-control, logging, and retention policies.
- Generated documents should be reviewed before real-world legal use.

---

## 31. Deployment

The frontend is deployed using Streamlit.

**Live Application:** https://legal-document-generator.streamlit.app/

The deployed application reads the required LLM configuration from Streamlit Secrets rather than storing credentials in the repository.

---

## 32. Git Workflow

Typical development workflow:

```bash
git status
git add .
git commit -m "update project"
git push origin main
```

When modifying `frontend/app.py` while working from the `backend` directory:

```bash
git add ../frontend/app.py
git commit -m "update streamlit app"
git push origin main
```

Do not commit:

```text
.env
venv/
__pycache__/
generated outputs containing sensitive data
API keys
```

---

## 33. End-to-End Summary

```text
Case Information PDF
        ↓
PDF text extraction
        ↓
Chunking
        ↓
LLM structured case extraction
        ↓
Pydantic CaseInformation
        ↓
Reference PDF analysis
        ↓
Pydantic DocumentStructure
        ↓
Content mapping
        ↓
LLM structured document generation
        ↓
Pydantic GeneratedDocument
        ↓
DOCX + PDF
        ↓
Deterministic validation
        ↓
Evaluation
        ↓
Evaluation report
        ↓
Token usage
```

The key engineering principle is:

```text
LLM for understanding + generation
Python for orchestration + exact validation
Pydantic for structured contracts
Reference documents for template knowledge
```

---

## 34. Live Demo

**Legal Document Generation & Evaluation Agent**

https://legal-document-generator.streamlit.app/

Upload the Case Information PDF, generate the Affidavit in Reply, inspect the extracted entities and evaluation results, and download the generated documents.
