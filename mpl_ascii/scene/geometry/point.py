from __future__ import annotations
from dataclasses import dataclass

from mpl_ascii.scene.fingerprint import Fingerprintable, f8

@dataclass(frozen=True)
class Point2d(Fingerprintable):
    x: float
    y: float

    def __add__(self, p: Point2d) -> Point2d:
        return Point2d(self.x + p.x, self.y + p.y)

    def __repr__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"

    def fingerprint(self) -> bytes:
        return f"pt({f8(self.x)},{f8(self.y)})".encode()
