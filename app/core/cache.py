"""
Cache abstraction. Uses Redis if REDIS_URL is configured, otherwise falls back
to a simple in-memory TTL cache - so the API runs with zero external
dependencies out of the box, and gains Redis for free once you wire it up.
"""

import json
import time
from typing import Any

from app.config import get_settings

settings = get_settings()

_redis_client = None
_memory_store: dict[str, tuple[float, str]] = {} # key -> (expires_at, json_value)

def _get_redis():
    global _redis_client
    if _redis_client is None and settings.redis_url:
        import redis.asyncio as redis # imported lazily so redis is optional

        _redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis_client

async def cache_get(key: str) -> Any | None:
    client = _get_redis()
    if client:
        raw = await client.get(key)
        return json.loads(raw) if raw else None

    entry = _memory_store.get(key)
    if not entry:
        return None
    expires_at, raw = entry
    if time.time() > expires_at:
        _memory_store.pop(key, None)
        return None
    return json.loads(raw)