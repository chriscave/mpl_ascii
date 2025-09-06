from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from mpl_ascii.scene.fingerprint import Fingerprintable
from mpl_ascii.scene.geometry.matrix import Matrix2d
from mpl_ascii.scene.geometry.point import Point2d


class Mapping2d(ABC):

    def __call__(self, other: Point2d) -> Point2d:
        raise NotImplementedError()


@dataclass(frozen=True)
class AffineMap2d(Fingerprintable, Mapping2d):
    linear: Matrix2d
    translation: Point2d

    def inverse(self) -> AffineMap2d:
        A_inv = self.linear.inverse()
        Ab = A_inv * self.translation
        b_inv = Point2d(-Ab.x, -Ab.y)
        return AffineMap2d(A_inv, b_inv)

    def fingerprint(self) -> bytes:
        return b"T(" + self.linear.fingerprint() + b"," + self.translation.fingerprint() + b")"

    def __call__(self, other: Point2d) -> Point2d:
        return self.linear * other + self.translation

    def __matmul__(self, other: AffineMap2d) -> AffineMap2d:
        new_A = self.linear @ other.linear
        new_b = self.linear * other.translation + self.translation
        return AffineMap2d(new_A, new_b)

    def __repr__(self) -> str:
        row1 = f"| {self.linear.a:4.3f}  {self.linear.b:4.3f} | + | {self.translation.x:4.3f} |"
        row2 = f"| {self.linear.c:4.3f}  {self.linear.d:4.3f} |   | {self.translation.y:4.3f} |"
        return f"{row1}\n{row2}"

