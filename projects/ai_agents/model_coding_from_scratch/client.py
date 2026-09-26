"""Small OpenAI-compatible chat client used by the from-scratch lessons.

This intentionally uses Python's standard-library urllib so students can see
what an SDK usually hides: JSON payload, HTTP headers, network request, and
response parsing.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROJECT_DIR.parents[2]
try:
    from dotenv import load_dotenv

    # Load the repository-root .env; fall back to this lesson's local .env.
    env_file = REPO_ROOT / ".env"
    if not env_file.exists():
        env_file = PROJECT_DIR / ".env"
    load_dotenv(env_file)
except ImportError:
    pass  # Environment variables can also be exported directly in the shell.

BASE_URL = os.getenv("AI_BASE_URL", "https://router.bynara.id/v1").rstrip("/")
API_KEY = os.getenv("AI_API_KEY", "").strip()
MODEL = os.getenv("AI_MODEL", "gpt-6-luna").strip()


class ModelAPIError(RuntimeError):
    """Raised when configuration, transport, or the model response is invalid."""


def chat(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.3,
    max_tokens: int = 500,
    json_mode: bool = False,
) -> tuple[str, dict[str, Any]]:
    """Send chat messages to an OpenAI-compatible endpoint.

    Args:
        messages: Ordered system/user/assistant messages.
        temperature: Lower is more repeatable; higher is more varied.
        max_tokens: Maximum generated response tokens.
        json_mode: Request JSON-only output when supported by the endpoint.

    Returns:
        A pair of (assistant text, usage metadata).

    Raises:
        ModelAPIError: If the key is missing or the endpoint returns bad data.
    """
    if not API_KEY:
        raise ModelAPIError(
            "AI_API_KEY is missing. Copy .env.example to .env in this folder "
            "and add your provider key."
        )

    payload: dict[str, Any] = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    request = Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise ModelAPIError(f"Provider returned HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError) as exc:
        raise ModelAPIError(f"Could not reach model endpoint: {exc}") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ModelAPIError("Provider response was not valid JSON/text.") from exc

    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ModelAPIError("Response did not contain choices[0].message.content.") from exc
    if not isinstance(content, str):
        raise ModelAPIError("The assistant content was not a text string.")
    return content, result.get("usage", {})
