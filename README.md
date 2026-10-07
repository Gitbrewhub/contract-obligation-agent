# Contract.AI — AI-Powered Contract Obligation Extraction & Risk-Aware Review

![Status](https://img.shields.io/badge/STATUS-RESEARCH%20PROTOTYPE-blue)
![Python](https://img.shields.io/badge/PYTHON-3.x-blue)
![Frontend](https://img.shields.io/badge/FRONTEND-REACT-61DAFB)
![Backend](https://img.shields.io/badge/BACKEND-FLASK-black)
![Workflow](https://img.shields.io/badge/WORKFLOW-LANGGRAPH-orange)
![Database](https://img.shields.io/badge/DATABASE-POSTGRESQL-336791)

Contract.AI is an AI-assisted contract intelligence system that extracts
structured contractual obligations from PDF and DOCX documents, verifies
the extracted information against supporting contract text, and generates
review-oriented risk signals.

The system combines LLM-based obligation extraction with deterministic
validation, source-grounded verification, and rule-based risk analysis to
make contract review more traceable and easier to inspect.

---

## 🚀 Key Features

### 📄 Contract Processing

- **PDF & DOCX Support:** Upload and process contract documents in PDF and DOCX formats.
- **Document Ingestion:** Extracts contract text for downstream analysis.
- **Structured Processing:** Converts unstructured contract content into structured obligation records.

### 🤖 AI-Powered Obligation Extraction

- **LLM-Based Extraction:** Uses an NVIDIA-hosted language model to identify contractual obligations.
- **Responsible Party:** Identifies the party associated with an obligation.
- **Deadline Extraction:** Extracts available deadlines associated with obligations.
- **Clause Reference:** Captures available clause or reference information.
- **Structured Output:** Converts model responses into a defined obligation schema.

### 🔍 Source-Grounded Verification

- **Semantic Verification:** Compares extracted obligations with relevant contract segments using Sentence-BERT embeddings.
- **Cosine Similarity:** Measures semantic similarity between extracted obligations and source text.
- **Lexical Overlap:** Uses textual overlap as an additional grounding signal.
- **Evidence Retrieval:** Identifies supporting contract text for extracted obligations.
- **Grounding Score:** Combines semantic similarity and lexical overlap to determine the strength of source support.

### ⚠️ Risk-Aware Review

- **Rule-Based Analysis:** Generates review-oriented risk signals using deterministic rules.
- **Clause Indicators:** Considers indicators such as indemnification, penalties, termination, and liability.
- **Deadline Proximity:** Considers detected deadline proximity when assigning risk tiers.
- **Verification Status:** Flags obligations that require additional review.
- **Risk Categories:** `HIGH` · `MEDIUM` · `LOW` · `REVIEW` · `NO_DEADLINE`

### 🔗 Evidence Traceability

- Links extracted obligations to supporting contract text.
- Displays grounding information alongside extracted results.
- Allows reviewers to inspect the source behind generated information.
- Separates LLM-based extraction from downstream verification and risk signalling.

### 🖥️ Web-Based Review Interface

- React/Vite frontend for reviewing processed contracts.
- Displays extracted obligations and associated metadata.
- Presents supporting evidence, verification status, grounding score, and risk signals.

---

## 🏗️ System Architecture

Contract.AI follows a modular, five-stage processing workflow orchestrated using **LangGraph**.

```text
                    Contract PDF / DOCX
                            │
                            ▼
                  ┌───────────────────┐
                  │     Ingestion     │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │  LLM Extraction   │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    Validation     │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    Verification   │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │   Risk Analysis   │
                  └─────────┬─────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ PostgreSQL + pgvector│
                 └──────────┬──────────┘
                            │
                            ▼
                     Flask REST API
                            │
                            ▼
                       React / Vite

---




## 🔄 Processing Pipeline

The Contract.AI processing pipeline transforms an uploaded contract into
structured, verified, and risk-aware obligation records.

```text
┌──────────────────────┐
│   Contract Upload    │
│      PDF / DOCX      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Ingestion       │
│  Extract Contract    │
│        Text          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Obligation          │
│     Extraction       │
│   NVIDIA LLM         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Validation      │
│   Schema / Format    │
│       Checks         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Semantic        │
│     Verification     │
│ Embeddings + Lexical │
│       Overlap        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Grounding Score   │
│  Semantic + Lexical  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Risk Analysis     │
│   Deterministic      │
│      Rules           │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Storage        │
│ PostgreSQL + pgvector│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Review Interface  │
│     React / Vite     │
└──────────────────────┘



Contract
   ↓
Text Extraction
   ↓
LLM Obligation Extraction
   ↓
Schema Validation
   ↓
Semantic + Lexical Verification
   ↓
Grounding Score
   ↓
Deterministic Risk Analysis
   ↓
PostgreSQL + pgvector
   ↓
Flask REST API
   ↓
React Review Interface

---

## 🧠 How It Works

Contract.AI processes each uploaded contract through five stages orchestrated using **LangGraph**.

### 1. 📄 Ingestion

The system accepts PDF and DOCX contracts and extracts their textual content using document parsing components.

The extracted text is prepared for downstream obligation extraction and source-grounded verification.

### 2. 🤖 Obligation Extraction

The extracted contract text is passed to an NVIDIA-hosted language model to identify contractual obligations.

The extraction stage produces structured information including:

- Responsible party
- Obligation text
- Deadline
- Clause/reference information

The LLM output is then passed to the validation stage rather than being directly stored as a final result.

### 3. ✅ Validation

The extracted obligation data is validated against the expected schema.

This stage checks whether the generated output has the required structure and fields before it proceeds to verification and persistence.

Keeping validation separate from extraction helps prevent malformed model responses from propagating through the pipeline.

### 4. 🔍 Source-Grounded Verification

The verification stage checks whether an extracted obligation is supported by the original contract text.

The system:

1. Generates embeddings for the extracted obligation and contract segments.
2. Calculates cosine similarity between them.
3. Calculates lexical overlap.
4. Combines both signals into a grounding score.
5. Retrieves the most relevant supporting contract text.
6. Assigns a verification status.

The grounding score is calculated as:

```text
Grounding Score =
0.70 × Semantic Similarity
+
0.30 × Lexical Overlap

---

## 🧰 Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, Vite |
| **Backend** | Python, Flask |
| **Workflow Orchestration** | LangGraph |
| **LLM** | NVIDIA-hosted Nemotron |
| **Embeddings** | Sentence-BERT |
| **Database** | PostgreSQL |
| **Vector Search** | pgvector |
| **Document Processing** | pypdf, python-docx |
| **API** | Flask REST API |
| **Infrastructure** | Docker |
| **Testing** | pytest |

### Core Technologies

**React + Vite**  
Provides the web-based interface for uploading contracts and reviewing extracted obligations, verification information, supporting evidence, and risk signals.

**Flask**  
Provides the backend REST API and connects the frontend with the contract-processing workflow.

**LangGraph**  
Orchestrates the five-stage processing workflow:

```text
Ingestion → Extraction → Validation → Verification → Risk

---

## 🖥️ Application Preview

Contract.AI provides a web-based interface for uploading contracts and reviewing extracted obligations, supporting evidence, verification information, and risk signals.

### 📄 Contract Upload

Upload a PDF or DOCX contract through the web interface to begin processing.

![Contract Upload](docs/screenshots/contract-upload.png)

### 📋 Obligation Review

Review extracted contractual obligations together with their responsible party, deadline, clause/reference information, and verification status.

![Obligation Review](docs/screenshots/obligation-review.png)

### 🔍 Evidence & Risk Review

Inspect the supporting contract text, grounding score, verification status, and review-oriented risk signal associated with each obligation.

![Evidence and Risk Review](docs/screenshots/evidence-risk-review.png)


---

## 📦 Installation & Setup

### Prerequisites

Make sure the following are installed:

- Python 3.x
- Node.js and npm
- Docker Desktop
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Gitbrewhub/contract-obligation-agent.git
cd contract-obligation-agent

### 2. Create the Python Environment

Create a virtual environment for the backend:

```bash
python -m venv .venv

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the required Python packages for the backend and processing pipeline.

> The project currently uses a local virtual environment for development.

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg://contract_user:contract_password@localhost:5432/contracts_db
NVIDIA_API_KEY=your_nvidia_api_key
```

Replace `your_nvidia_api_key` with your NVIDIA API key.

> **Security:** Never commit `.env` files, API keys, database passwords, or other secrets to GitHub.

### 5. Start PostgreSQL

Contract.AI uses PostgreSQL with pgvector for persistent storage and semantic similarity operations.

Start the PostgreSQL container:

```powershell
docker compose up -d postgres
```

Verify that the container is running:

```powershell
docker ps
```

The PostgreSQL service runs on:

```text
localhost:5432
```

### 6. Start the Backend

From the project root:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python backend\app.py
```

The Flask backend will be available at:

```text
http://127.0.0.1:5000
```

### 7. Verify the Backend

Open a second terminal and run:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
```

A successful response should indicate:

```text
status        : ok
service       : contract-obligation-agent
orchestration : langgraph
```

### 8. Start the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite will display the local development URL, typically:

```text
http://localhost:5173
```

Open the displayed URL in your browser to access the Contract.AI interface.

### 9. Process a Contract

Once the backend and frontend are running:

1. Open the Contract.AI web interface.
2. Upload a PDF or DOCX contract.
3. Start contract processing.
4. The document passes through the LangGraph workflow.
5. Contractual obligations are extracted and validated.
6. Extracted obligations are compared against supporting contract text.
7. Verification and grounding information is generated.
8. Deterministic risk signals are calculated.
9. Results are stored in PostgreSQL.
10. The extracted obligations and review information are displayed in the frontend.



---

## 🖥️ Application Preview

Contract.AI provides a web-based interface for uploading contracts and reviewing extracted obligations, verification information, supporting evidence, and risk signals.

### 📄 Contract Upload

Upload a PDF or DOCX contract through the web interface to begin processing.

> Screenshot will be added here.

### 📋 Obligation Review

Review extracted contractual obligations together with their responsible party, deadline, clause/reference information, and verification status.

> Screenshot will be added here.

### 🔍 Evidence & Risk Review

Inspect the supporting contract text, grounding score, verification status, and review-oriented risk signal associated with each obligation.

> Screenshot will be added here


---

## 🔌 API

Contract.AI exposes a Flask-based REST API for backend communication and contract processing.

### Health Check

```http
GET /health

### Health Check

```http
GET /health
```

paste this:

````markdown
Returns the current backend service status and confirms that the LangGraph workflow is available.

**Example response:**

```json
{
  "status": "ok",
  "service": "contract-obligation-agent",
  "orchestration": "langgraph"
}
```

### Upload Contract

```http
POST /contracts/upload
```

Uploads a PDF or DOCX contract for processing.

The backend stores the uploaded document and sends it through the contract-processing workflow.

**Supported formats:**

```text
.pdf
.docx
```

### Retrieve Obligations

```http
GET /contracts/<contract_id>/obligations
```

Retrieves the obligations extracted from a processed contract.

Replace `<contract_id>` with the ID of the processed contract.

**Example:**

```http
GET /contracts/68/obligations
```

The response contains the extracted obligation information, including available metadata such as:

- Obligation text
- Responsible party
- Deadline
- Clause/reference
- Verification status
- Grounding score
- Supporting evidence
- Risk signal

### API Workflow

```text
React Frontend
      │
      ▼
POST /contracts/upload
      │
      ▼
Flask REST API
      │
      ▼
LangGraph Processing Workflow
      │
      ▼
PostgreSQL + pgvector
      │
      ▼
GET /contracts/<contract_id>/obligations
      │
      ▼
React Review Interface
```


---

## 📁 Project Structure

```text
contract-obligation-agent/
│
├── agents/                  # AI-based obligation extraction
├── backend/                 # Flask REST API
├── contracts/               # Contract files and uploads
├── database/                # PostgreSQL database configuration
├── docs/                    # Project documentation
├── evaluation/              # Evaluation utilities
├── frontend/                # React/Vite frontend
├── graph/                   # LangGraph workflow
├── ingestion/               # Document ingestion and parsing
├── pipeline/                # Contract processing components
├── tests/                   # Automated tests
├── utils/                   # Supporting utilities
│
├── .gitignore
├── docker-compose.yml
├── .env                     # Local environment configuration
└── README.md
```

### Core Components

| Directory | Purpose |
|---|---|
| `agents/` | Obligation extraction and AI processing components |
| `backend/` | Flask REST API and application entry point |
| `contracts/` | Contract documents and upload handling |
| `database/` | Database connection and persistence |
| `docs/` | Project documentation and supporting materials |
| `evaluation/` | Evaluation and analysis utilities |
| `frontend/` | React/Vite web interface |
| `graph/` | LangGraph workflow orchestration |
| `ingestion/` | PDF/DOCX document ingestion and parsing |
| `pipeline/` | Contract processing pipeline components |
| `tests/` | Automated and component-level tests |
| `utils/` | Shared utility functions |


---

## 🧪 Testing & Results

Contract.AI was tested at both the component level and through end-to-end contract processing runs.

### Functional Testing

The implemented system was tested across the following components:

- Document loading and parsing
- Contract ingestion
- Obligation extraction
- Schema validation
- Semantic verification
- Risk signal generation
- PostgreSQL persistence
- Flask API endpoints
- React frontend integration

### End-to-End Processing

Successful end-to-end processing runs were observed during development:

| Run | Contract ID | Obligations Generated | HTTP Status |
|---|---:|---:|---:|
| 1 | 65 | 19 | 201 |
| 2 | 68 | 20 | 201 |

These runs demonstrate that the implemented pipeline can process contract documents and return structured obligation results through the backend API.

### Verification Process

The verification stage combines semantic similarity and lexical overlap to provide a source-grounding signal.

```text
Extracted Obligation
        │
        ▼
Semantic Similarity
        │
        ├──────────────┐
        ▼              ▼
Lexical Overlap    Supporting Text
        │
        ▼
  Grounding Score
        │
        ▼
Verification Status
```

The grounding score is calculated as:

```text
Grounding Score =
0.70 × Semantic Similarity
+
0.30 × Lexical Overlap
```

### Risk Signal Testing

The deterministic risk engine considers:

- Verification status
- Deadline proximity
- Contractual clause indicators

The current risk categories are:

```text
HIGH
MEDIUM
LOW
REVIEW
NO_DEADLINE
```

### Evaluation Status

The current implementation demonstrates functional end-to-end operation. However, a dedicated annotated evaluation dataset has not yet been used to establish quantitative accuracy.

Therefore, the current results do **not** claim:

- Precision
- Recall
- F1-score
- Verification accuracy
- False-positive rate
- Generalized model accuracy

Processing latency and token usage have also not been systematically benchmarked.

> The reported runs are functional validation results and should not be interpreted as formal accuracy benchmarks.


---

## 💡 Design Decisions

### 1. LLM-Based Extraction with Deterministic Downstream Processing

The system uses an NVIDIA-hosted language model for understanding contract language and extracting structured obligations.

The extracted output is then passed through separate validation, verification, and risk-analysis stages rather than being treated as the final result.

This separation makes the downstream processing more transparent and easier to inspect.

### 2. LangGraph Workflow Orchestration

LangGraph is used to orchestrate the contract-processing workflow as explicit stages:

```text
Ingestion
    ↓
Extraction
    ↓
Validation
    ↓
Verification
    ↓
Risk
```

This modular structure allows individual stages to be tested, debugged, and extended independently.

### 3. Source-Grounded Verification

The system does not rely solely on the generated obligation.

Each extracted obligation is compared against contract segments to identify supporting source text.

The verification stage uses:

- Sentence-BERT embeddings
- Cosine similarity
- Lexical overlap
- Grounding score

This provides reviewers with evidence that can be inspected alongside the extracted obligation.

### 4. Combined Grounding Score

Semantic similarity and lexical overlap are combined into a single grounding score:

```text
Grounding Score =
0.70 × Semantic Similarity
+
0.30 × Lexical Overlap
```

The combined score provides a practical source-grounding signal while retaining both semantic and textual evidence.

### 5. Deterministic Risk Signals

Risk analysis is implemented separately from LLM generation.

The risk engine considers:

- Verification status
- Deadline proximity
- Contractual clause indicators

The resulting categories are:

```text
HIGH
MEDIUM
LOW
REVIEW
NO_DEADLINE
```

These categories are intended as review-oriented signals rather than legal conclusions.

### 6. Human-Review-Oriented Design

The system presents extracted obligations together with supporting evidence, verification information, grounding scores, and risk signals.

This design keeps the reviewer in the decision-making loop instead of treating the generated output as an autonomous legal decision.


---

## ⚠️ Limitations

The current implementation has several limitations:

- **LLM Dependence:** Extracted obligations may contain errors or incomplete information and should be reviewed by a human.
- **Semantic Verification:** Semantic similarity provides a source-grounding signal but does not guarantee formal contractual entailment.
- **Risk Coverage:** The deterministic risk engine covers a defined set of clause indicators and deadline-based conditions and may not capture every possible contractual risk.
- **Evaluation Dataset:** A dedicated annotated obligation-level dataset has not yet been used to establish quantitative extraction and verification performance.
- **Limited Accuracy Metrics:** Precision, recall, F1-score, verification accuracy, and false-positive rates have not yet been systematically measured.
- **Document Scope:** The current system focuses on PDF and DOCX contract documents.
- **Deadline Dependency:** Deadline-based risk signals depend on the successful extraction of deadline information from the contract.
- **Generalization:** The current functional results are based on a limited number of end-to-end processing runs and should not be interpreted as evidence of generalized performance.
- **Legal Decision-Making:** The system provides review-oriented information and does not replace professional legal judgment.

These limitations define the scope of the current research prototype and provide directions for further evaluation and development.


---

## 🔮 Future Work

Future development of Contract.AI will focus on improving evaluation, verification, risk analysis, and scalability.

### 📊 Quantitative Evaluation

Develop a dedicated annotated obligation-level dataset to systematically evaluate:

- Precision
- Recall
- F1-score
- Verification accuracy
- False-positive rates
- Processing latency

### 🔍 Improved Verification

Explore entailment-based verification methods to complement the current embedding-based similarity and lexical-overlap approach.

ContractNLI-style evidence-based reasoning is a potential direction for determining whether extracted obligations are actually supported by contractual statements.

### ⚠️ Expanded Risk Analysis

Extend the deterministic risk engine to incorporate additional contractual conditions and more detailed review-oriented risk signals.

### 🧑‍⚖️ Human Review Evaluation

Conduct a human-review study to evaluate whether source-grounded evidence, grounding scores, and risk signals improve the effectiveness and confidence of contract reviewers.

### 📈 Scalability and Robustness

Evaluate the system on larger and more diverse collections of contracts to assess its robustness across different document structures, contract types, and contractual domains.

### 🔗 Enhanced Contract Intelligence

Future versions can explore additional contract-analysis capabilities such as improved clause understanding, richer evidence retrieval, and more comprehensive obligation tracking.

---

## 📜 License

This project is currently provided as a research prototype.

A formal open-source license will be added in a future release.


