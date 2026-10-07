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



### Important

For now, **don't add an image architecture diagram here** unless you already have the final one uploaded to GitHub.

The Mermaid/ASCII-style diagram above is enough for the first version.

Also, don't say:

> "five autonomous AI agents"

Your actual architecture is better described as:

> **"a five-stage LangGraph workflow"**

because your stages are not all independent AI agents.

---

### Your README now has this flow

```text
# Contract.AI
        ↓
🚀 Key Features
        ↓
🏗️ System Architecture
        ↓
NEXT → 🧠 How It Works
