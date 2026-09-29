import re
from typing import Dict, Any

from ingestion.embedder import generate_embedding


# Common words that do not provide much evidence when comparing
# an extracted obligation with its source contract passage.
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "by",
    "from",
    "at",
    "as",
    "is",
    "are",
    "be",
    "shall",
    "will",
    "must",
    "may",
    "this",
    "that",
    "these",
    "those",
    "their",
    "its",
    "all",
    "any",
    "such",
    "within",
    "under",
    "during",
    "before",
    "after",
}


def cosine_similarity(embedding_a, embedding_b) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """
    if not embedding_a or not embedding_b:
        return 0.0

    if len(embedding_a) != len(embedding_b):
        raise ValueError("Embedding dimensions must match")

    dot_product = sum(
        a * b
        for a, b in zip(embedding_a, embedding_b)
    )

    magnitude_a = sum(
        a * a
        for a in embedding_a
    ) ** 0.5

    magnitude_b = sum(
        b * b
        for b in embedding_b
    ) ** 0.5

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def normalize_text(text: str) -> str:
    """
    Normalize text for lexical comparison.
    """
    if not text:
        return ""

    text = text.lower()

    # Keep words and numbers.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Collapse whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def meaningful_tokens(text: str) -> set:
    """
    Extract meaningful tokens while removing common stopwords.
    """
    normalized = normalize_text(text)

    if not normalized:
        return set()

    tokens = normalized.split()

    return {
        token
        for token in tokens
        if token not in STOPWORDS and len(token) > 2
    }


def lexical_overlap(
    obligation_text: str,
    source_text: str,
) -> float:
    """
    Calculate how much of the meaningful obligation vocabulary
    appears in the retrieved source passage.

    Returns a value between 0 and 1.
    """
    obligation_tokens = meaningful_tokens(obligation_text)
    source_tokens = meaningful_tokens(source_text)

    if not obligation_tokens or not source_tokens:
        return 0.0

    overlap = obligation_tokens.intersection(source_tokens)

    return len(overlap) / len(obligation_tokens)


def verify_obligation(
    obligation_text: str,
    source_text: str,
) -> Dict[str, Any]:
    """
    Verify whether an extracted obligation is grounded in a
    retrieved contract passage.

    Verification uses two signals:

    1. Semantic similarity
       Measures conceptual similarity using embeddings.

    2. Lexical overlap
       Measures whether important words from the obligation
       actually occur in the source passage.

    The two signals are combined into a grounding score.
    """

    if not obligation_text or not obligation_text.strip():
        return {
            "verified": False,
            "verification_status": "NOT_VERIFIED",
            "grounding_score": 0.0,
            "semantic_score": 0.0,
            "lexical_score": 0.0,
            "source_text": source_text or "",
            "reason": "Obligation text is empty.",
        }

    if not source_text or not source_text.strip():
        return {
            "verified": False,
            "verification_status": "NOT_VERIFIED",
            "grounding_score": 0.0,
            "semantic_score": 0.0,
            "lexical_score": 0.0,
            "source_text": "",
            "reason": "No source contract passage was available.",
        }

    # ---------------------------------------------------------
    # 1. Semantic similarity
    # ---------------------------------------------------------

    obligation_embedding = generate_embedding(
        obligation_text
    )

    source_embedding = generate_embedding(
        source_text
    )

    semantic_score = cosine_similarity(
        obligation_embedding,
        source_embedding,
    )

    # ---------------------------------------------------------
    # 2. Lexical overlap
    # ---------------------------------------------------------

    lexical_score = lexical_overlap(
        obligation_text,
        source_text,
    )

    # ---------------------------------------------------------
    # 3. Combined grounding score
    # ---------------------------------------------------------

    # Semantic similarity carries more weight because wording
    # can differ while the contractual meaning remains similar.
    grounding_score = (
        0.70 * semantic_score
        + 0.30 * lexical_score
    )

    grounding_score = max(
        0.0,
        min(1.0, grounding_score),
    )

    # ---------------------------------------------------------
    # 4. Verification decision
    # ---------------------------------------------------------

    # Strong semantic match.
    strong_semantic_match = semantic_score >= 0.60

    # Moderate semantic match supported by textual evidence.
    supported_match = (
        semantic_score >= 0.45
        and lexical_score >= 0.30
    )

    verified = (
        strong_semantic_match
        or supported_match
    )

    verification_status = (
        "VERIFIED"
        if verified
        else "NOT_VERIFIED"
    )

    # ---------------------------------------------------------
    # 5. Explanation
    # ---------------------------------------------------------

    if strong_semantic_match:
        reason = (
            "The obligation has strong semantic similarity "
            "with the retrieved source passage."
        )

    elif supported_match:
        reason = (
            "The obligation has moderate semantic similarity "
            "and sufficient textual overlap with the retrieved "
            "source passage."
        )

    else:
        reason = (
            "The extracted obligation has insufficient semantic "
            "and textual similarity with the retrieved source "
            "passage."
        )

    return {
        "verified": verified,
        "verification_status": verification_status,
        "grounding_score": round(
            float(grounding_score),
            4,
        ),
        "semantic_score": round(
            float(semantic_score),
            4,
        ),
        "lexical_score": round(
            float(lexical_score),
            4,
        ),
        "source_text": source_text,
        "reason": reason,
    }


def verify_with_nvidia(
    obligation_text: str,
    source_text: str,
) -> Dict[str, Any]:
    """
    Backward-compatible wrapper.

    The verification stage no longer calls NVIDIA.
    NVIDIA is used for obligation extraction, while
    deterministic + embedding-based verification is used
    for grounding.
    """
    return verify_obligation(
        obligation_text=obligation_text,
        source_text=source_text,
    )