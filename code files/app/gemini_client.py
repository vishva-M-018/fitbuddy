import time
from functools import lru_cache

from google import genai

from .config import settings


class GeminiUnavailable(RuntimeError):
    pass


@lru_cache
def get_client():
    if not settings.gemini_api_key:
        raise GeminiUnavailable(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    model: str,
    prompt: str,
    max_output_tokens: int = 4000
) -> str:

    client = get_client()

    max_retries = 3
    delay = 2

    for attempt in range(max_retries + 1):

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "max_output_tokens": max_output_tokens,
                },
            )

            text = getattr(response, "text", None)

            if not text:
                raise GeminiUnavailable(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as exc:

            error_text = str(exc)

            retryable = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            )

            if not retryable or attempt >= max_retries:
                raise GeminiUnavailable(
                    f"Gemini request failed: {error_text}"
                ) from exc

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {delay} seconds..."
            )

            time.sleep(delay)

            delay *= 2