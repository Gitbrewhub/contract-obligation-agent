import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_BASE_URL = os.getenv(
    "NVIDIA_BASE_URL",
    "https://integrate.api.nvidia.com/v1",
)

NVIDIA_MODEL = os.getenv(
    "NVIDIA_MODEL",
    "nvidia/nemotron-3.5-lightning-30b-a3b",
)


if not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY is not set in .env"
    )


client = OpenAI(
    base_url=NVIDIA_BASE_URL,
    api_key=NVIDIA_API_KEY,
)


def ask_nvidia(prompt: str) -> str:
    """
    Send a structured request to NVIDIA NIM.

    This function is intentionally generic.
    Individual agents are responsible for their prompts
    and response validation.
    """

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty"
        )

    response = client.chat.completions.create(
        model=NVIDIA_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a contract intelligence API. "
                    "Follow the user's requested output format exactly. "
                    "Do not provide unnecessary explanations."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.0,
        max_tokens=4000,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
    )

    if not response.choices:
        raise ValueError(
            "NVIDIA returned no choices"
        )

    content = response.choices[0].message.content

    if not content or not content.strip():
        raise ValueError(
            "NVIDIA returned an empty response"
        )

    return content.strip()