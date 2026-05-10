import logging

from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: OpenAI | None = None


def get_openai_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def chat_completion(prompt: str) -> str:
    """Send a single user prompt and return the assistant's reply."""
    client = get_openai_client()
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content or ""
    logger.debug("OpenAI response: %s", content[:200])
    return content
