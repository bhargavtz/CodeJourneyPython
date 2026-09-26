"""From-scratch model calls: the smallest useful AI program."""
from __future__ import annotations

import json
from typing import Any

from .client import chat


def basic_call(question: str) -> str:
    """Ask one question and return the model's text answer."""
    answer, _ = chat([{"role": "user", "content": question}])
    return answer


def conversation(question: str, history: list[dict[str, str]] | None = None) -> tuple[str, list[dict[str, str]]]:
    """Continue a conversation by explicitly resending its message history."""
    messages = list(history or [])
    messages.append({"role": "user", "content": question})
    answer, _ = chat(messages)
    messages.append({"role": "assistant", "content": answer})
    return answer, messages


def classify_support_message(message: str) -> dict[str, Any]:
    """Classify support text into a small JSON object.

    This is deliberately a lesson, not production-grade validation. The next
    lesson can add a schema library or stricter validators.
    """
    system = (
        "You are a support classifier. Return ONLY one JSON object with these keys: "
        "category (billing, technical, account, other), "
        "urgency (low, medium, high), and summary (under 12 words). "
        "Do not invent facts."
    )
    raw, _ = chat(
        [{"role": "system", "content": system}, {"role": "user", "content": message}],
        temperature=0,
        max_tokens=180,
        json_mode=True,
    )
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model did not return valid JSON: {raw[:200]}") from exc
    allowed = {"category", "urgency", "summary"}
    if set(value) != allowed:
        raise ValueError(f"Unexpected JSON keys: {set(value)}")
    if value["category"] not in {"billing", "technical", "account", "other"}:
        raise ValueError("Unexpected category")
    if value["urgency"] not in {"low", "medium", "high"}:
        raise ValueError("Unexpected urgency")
    return value


if __name__ == "__main__":
    print(basic_call("Explain an API call in two simple sentences."))
    result = classify_support_message("I was charged twice and need a refund today.")
    print(json.dumps(result, indent=2))
