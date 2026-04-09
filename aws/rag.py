from __future__ import annotations

import asyncio
import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np

@dataclass(frozen = True)
class Chunk:
    doc_id: str
    chunk_id: str
    text: str

class LRUCacheTTL:
    def __init__(self, max_size: int = 128, ttl_seconds: int = 300)-> None:
        if max_size <= 0:
            raise ValueError("max_size mast be > 0")
        if ttl_seconds <= 0:
            raise ValueError("ttl seconds must be > 0")
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._d: "OrderedDict[str, Tuple[float, str]]" = OrderedDict()

    def _now(self) -> float:
        return time.time()
    
    def _purge_expired(self) -> None:
        now = self._now()
        expired = [k for k, (exp, _) in self._d.items() if exp <= now]
        for k in expired:
            self._d.pop(k, None)

    def get(self, key:str) -> Optional[str]:
        self._purge_expired()
        item = self._d.get(key)
        if item is None:
            return None
        exp, val = item
        if exp <= self._now():
            self._d.pop(key, None)
            return None
        self._d.move_to_end(key, last= True)
        return val
    
    def set(self, key: str, value: str) -> None:
        self._purge_expired()
        exp = self._now() + self.ttl_seconds
        self._d[key] = (exp, value)
        self._d.move_to_end(key, last = True)
        while len(self._d) > self.max_size:
            self._d.popitem(last= False)

def _stable_seed(text: str) -> int:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") & 0xFFFFFFFF

def fake_embedding(text: str, dim: int = 128) -> np.ndarray:
    rng = np.random.RandomState(_stable_seed(text))
    v = rng.standard_normal(size=(dim,)).astype(np.float32)
    n = float(np.linalg.norm(v))
    if n == 0.0:
        return v
    return v / n


def fake_llm(retrieved_context: str) -> str:
    return f"Answer based on : {retrieved_context}"

def chunk_text(content: str, chunk_size: int = 200) -> List[str]:
    content = content.strip()
    if not content:
        return []
    out: List[str] = []
    for i in range(0, len(content), chunk_size):
        out.append(content[i : i + chunk_size])
    return out

class RAGService:
    def __init__(
        self,
        *,
        chunk_size: int = 200,
        embedding_dim: int = 128,
        top_k: int = 3,
        cache_max_size: int = 128,
        cache_ttl_seconds: int = 300,
    ) -> None:
        self.chunk_size = chunk_size
        self.embedding_dim = embedding_dim
        self.top_k = top_k

        self.chunks: List[Chunk] = []
        self.embs: List[np.ndarray] = []
        self._cache = LRUCacheTTL(max_size = cache_max_size, ttl_seconds= cache_ttl_seconds)
        self._lock = asyncio.Lock()

    def add_document(self, doc_id: str, content: str) -> None:
        if not isinstance(doc_id, str) or not doc_id.strip():
            raise ValueError("doc_id must be a non-empty string")
        if not isinstance(content, str) or not content.strip():
            return
        
        pieces = chunk_text
    


