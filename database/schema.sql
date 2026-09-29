CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS contracts (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER NOT NULL
        REFERENCES contracts(id)
        ON DELETE CASCADE,

    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,

    embedding VECTOR(384),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS obligations (
    id SERIAL PRIMARY KEY,
    contract_id INTEGER NOT NULL
        REFERENCES contracts(id)
        ON DELETE CASCADE,

    party_responsible TEXT,
    obligation_text TEXT NOT NULL,
    deadline TEXT,
    clause_reference TEXT,

    verification_status TEXT DEFAULT 'PENDING',
    grounding_score FLOAT,

    risk_tier TEXT,
    days_until_deadline INTEGER,

    source_chunk_id INTEGER
        REFERENCES document_chunks(id)
        ON DELETE SET NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);