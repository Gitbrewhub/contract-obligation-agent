# Contract.AI

## AI-Powered Contract Obligation Extraction, Verification, and Risk-Aware Review

Contract.AI is an AI-assisted contract intelligence system that extracts structured obligations from PDF and DOCX contracts and connects each extracted obligation to supporting contract evidence.

The system combines LLM-based extraction with deterministic validation, source-grounded verification, and rule-based risk signalling to make contract review more traceable and easier to inspect.

> **Core principle:** LLM-generated contract information should be checked against the source document before being relied upon.

---

## Overview

Contracts contain important obligations, deadlines, responsible parties, and contractual conditions that can be difficult to identify manually.

Contract.AI provides a workflow for:

- Uploading PDF and DOCX contracts
- Extracting contract text
- Identifying contractual obligations using an NVIDIA-hosted LLM
- Validating extracted information against a defined schema
- Verifying extracted obligations against the original contract text
- Generating review-oriented risk signals
- Storing obligations and supporting evidence in PostgreSQL
- Presenting results through a React-based web interface

The system is designed as a **review-support tool**, not as a replacement for legal judgment.

---

# System Workflow

```text
                Contract PDF / DOCX
                        │
                        ▼
                ┌───────────────┐
                │   Ingestion   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │  LLM-Based    │
                │   Extraction  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   Validation  │
                │   + Schema    │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   Semantic    │
                │ Verification  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │  Risk Signal  │
                │    Engine     │
                └───────┬───────┘
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
                  React / Vite UI
