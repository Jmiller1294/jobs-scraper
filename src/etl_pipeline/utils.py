import asyncio
import time
from collections import deque


class AsyncAPIKeyManager:
  def __init__(self, keys: list[str]):
    self._keys = deque(keys)
    self._lock = asyncio.Lock()

    # key -> timestamp when usable again
    self._unavailable_until: dict[str, float] = {}

    # optional: track daily usage
    self._usage: dict[str, int] = {k: 0 for k in keys}

  async def get_key(self) -> str:
    async with self._lock:
      now = time.time()

      for _ in range(len(self._keys)):
        key = self._keys[0]
        self._keys.rotate(-1)

        if now >= self._unavailable_until.get(key, 0):
          self._usage[key] += 1
          return key

        raise RuntimeError("All API keys are exhausted or rate-limited")

  async def mark_rate_limited(self, key: str):
    async with self._lock:
      self._unavailable_until[key] = time.time() + 60  # 1 min

  async def mark_daily_limited(self, key: str):
    async with self._lock:
      self._unavailable_until[key] = time.time() + 86400  # 24 hrs