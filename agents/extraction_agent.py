import json
import re

from agents.nvidia_client import ask_nvidia


EXTRACTION_PROMPT = """
You are a contract obligation extraction system.

Analyze the contract text below and identify every explicit
contractual obligation.

For each obligation, extract exactly these fields:

- party_responsible
- obligation_text
- deadline
- clause_reference

Rules:
1. Extract only obligations explicitly supported by the source text.
2. Do not invent information.
3. If a deadline is not explicitly stated, use null.
4. If a clause reference is not explicitly available, use null.
5. Keep obligation_text faithful to the source.
6. Return exactly ONE complete JSON array.
7. Return an empty JSON array [] if there are no obligations.
8. Do not return reasoning.
9. Do not return Markdown.
10. Do not use code fences.
11. Do not use <think> or </think>.
12. Do not return multiple JSON arrays.
13. Complete the entire JSON response before stopping.
14. Do not truncate the JSON.
15. Keep the reason for each obligation out of the response.
16. Return no fields other than the four requested fields.

Expected structure:

[
  {
    "party_responsible": "Supplier",
    "obligation_text": "Submit the monthly progress report",
    "deadline": "within ten business days after the end of each month",
    "clause_reference": "4.2"
  }
]

SOURCE CONTRACT TEXT:
--------------------
__CONTRACT_CHUNK__
--------------------
"""


def _build_extraction_prompt(chunk: str) -> str:
    """
    Insert the contract text into the prompt without using
    str.format(), so JSON braces in the prompt can never
    become accidental format placeholders.
    """

    return EXTRACTION_PROMPT.replace(
        "__CONTRACT_CHUNK__",
        chunk,
    )


def _remove_thinking_sections(text: str) -> str:
    """
    Remove reasoning/thinking sections if the model returns them.
    """

    # Remove complete <think>...</think> sections.
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # If an unmatched </think> appears, keep only what follows it.
    if "</think>" in text.lower():

        matches = list(
            re.finditer(
                r"</think>",
                text,
                flags=re.IGNORECASE,
            )
        )

        if matches:
            text = text[
                matches[-1].end():
            ]

    # Remove unmatched opening marker.
    text = re.sub(
        r"<think>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text.strip()


def _extract_complete_json_array(
    response: str,
) -> str:
    """
    Extract the first complete JSON array from the model response.

    This parser understands JSON strings, so brackets inside
    obligation text do not incorrectly terminate the array.
    """

    if not response or not response.strip():
        raise ValueError(
            "NVIDIA returned an empty extraction response"
        )

    cleaned = response.strip()

    # Remove reasoning.
    cleaned = _remove_thinking_sections(
        cleaned
    )

    # Remove Markdown fences.
    cleaned = re.sub(
        r"```(?:json)?",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = cleaned.replace(
        "```",
        "",
    ).strip()

    # Find the opening JSON array.
    start = cleaned.find("[")

    if start == -1:
        raise ValueError(
            "NVIDIA response does not contain a JSON array. "
            f"Response: {cleaned}"
        )

    depth = 0
    in_string = False
    escaped = False

    for index in range(
        start,
        len(cleaned),
    ):

        char = cleaned[index]

        if escaped:
            escaped = False
            continue

        if char == "\\" and in_string:
            escaped = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "[":
            depth += 1

        elif char == "]":
            depth -= 1

            if depth == 0:
                return cleaned[
                    start:index + 1
                ]

    raise ValueError(
        "NVIDIA returned an incomplete JSON array. "
        "The response ended before the closing ']'."
    )


def _sanitize_json_string_controls(
    json_text: str,
) -> str:
    """
    Convert raw control characters occurring inside JSON strings
    into valid escaped characters.
    """

    output = []

    in_string = False
    escaped = False

    for char in json_text:

        if escaped:
            output.append(char)
            escaped = False
            continue

        if char == "\\" and in_string:
            output.append(char)
            escaped = True
            continue

        if char == '"':
            output.append(char)
            in_string = not in_string
            continue

        if in_string:

            if char == "\n":
                output.append("\\n")
                continue

            if char == "\r":
                output.append("\\r")
                continue

            if char == "\t":
                output.append("\\t")
                continue

            if ord(char) < 32:
                continue

        output.append(char)

    return "".join(output)


def clean_json_response(
    response: str,
) -> str:
    """
    Clean and extract a complete JSON array.
    """

    json_text = _extract_complete_json_array(
        response
    )

    json_text = _sanitize_json_string_controls(
        json_text
    )

    return json_text.strip()


def extract_obligations(
    chunk: str,
) -> list[dict]:
    """
    Extract contractual obligations from one contract chunk
    using NVIDIA NIM.
    """

    if not chunk or not chunk.strip():
        raise ValueError(
            "Contract chunk cannot be empty"
        )

    prompt = _build_extraction_prompt(
        chunk
    )

    response = ask_nvidia(
        prompt
    )

    cleaned_response = clean_json_response(
        response
    )

    try:
        obligations = json.loads(
            cleaned_response
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            "NVIDIA returned invalid extraction JSON: "
            f"{cleaned_response}"
        ) from exc

    if not isinstance(
        obligations,
        list,
    ):
        raise ValueError(
            "NVIDIA extraction response must be a JSON array"
        )

    for item in obligations:

        if not isinstance(
            item,
            dict,
        ):
            raise ValueError(
                "Each extracted obligation must be a JSON object"
            )

        if "obligation_text" not in item:
            raise ValueError(
                "Extracted obligation is missing "
                "'obligation_text'"
            )

    return obligations