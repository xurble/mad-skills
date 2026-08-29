from __future__ import annotations

import copy
import secrets
import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass

from .preview import PreviewSpec


@dataclass(frozen=True)
class StoredPreview:
    spec: PreviewSpec
    expires_at: float


class PreviewStore:
    def __init__(
        self,
        *,
        max_previews: int = 64,
        ttl_seconds: int = 300,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.max_previews = min(max(1, max_previews), 64)
        self.ttl_seconds = min(max(1, ttl_seconds), 300)
        self._clock = clock
        self._items: OrderedDict[str, StoredPreview] = OrderedDict()
        self._lock = threading.Lock()

    def create(self, spec: PreviewSpec) -> str:
        with self._lock:
            self._prune_locked()
            while len(self._items) >= self.max_previews:
                self._items.popitem(last=False)
            preview_id = secrets.token_urlsafe(24)
            while preview_id in self._items:
                preview_id = secrets.token_urlsafe(24)
            self._items[preview_id] = StoredPreview(copy.deepcopy(spec), self._clock() + self.ttl_seconds)
            return preview_id

    def get(self, preview_id: str) -> PreviewSpec | None:
        with self._lock:
            self._prune_locked()
            item = self._items.get(preview_id)
            return copy.deepcopy(item.spec) if item else None

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def __len__(self) -> int:
        with self._lock:
            self._prune_locked()
            return len(self._items)

    def _prune_locked(self) -> None:
        now = self._clock()
        expired = [preview_id for preview_id, item in self._items.items() if item.expires_at <= now]
        for preview_id in expired:
            del self._items[preview_id]


preview_store = PreviewStore()
