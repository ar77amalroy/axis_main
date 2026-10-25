"""LLM helper – thin wrapper around AsyncOpenAI pointed at Gemini."""

import asyncio
import json
import re

from openai import AsyncOpenAI, RateLimitError

from app.config import settings

_client = AsyncOpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
)

_MAX_RETRIES = 3
_BACKOFF = [2, 4, 8]


async def _call(system: str, user: str) -> str:
    """Send a chat completion and return the raw assistant text."""
    for attempt in range(_MAX_RETRIES + 1):
        try:
            resp = await _client.chat.completions.create(
                model=settings.LLM_MODEL,
                temperature=0.2,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return resp.choices[0].message.content.strip()
        except RateLimitError:
            if attempt < _MAX_RETRIES:
                await asyncio.sleep(_BACKOFF[attempt])
            else:
                raise RuntimeError("LLM rate limit reached")


async def chat_text(system: str, user: str) -> str:
    """Return plain-text LLM response."""
    return await _call(system, user)


async def chat_json(system: str, user: str) -> dict:
    """Return parsed JSON from LLM response. Strips ```json fences."""
    raw = await _call(system, user)
    # Strip markdown code fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned invalid JSON: {exc}\nRaw: {raw[:500]}")
