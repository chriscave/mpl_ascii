from __future__ import annotations
from abc import ABC, abstractmethod
from hashlib import sha256
from typing import Iterable

ROUND = 8  # float precision for stable IDs

def f8(x: float) -> float:
    return round(float(x), ROUND)

def combine(parts: Iterable[bytes]) -> str:
    h = sha256()
    for p in parts:
        h.update(b"|")  # delimiter to avoid ambiguity
        h.update(p)
    return h.hexdigest()

class Fingerprintable(ABC):

    @abstractmethod
    def fingerprint(self) -> bytes:
        raise NotImplementedError()
