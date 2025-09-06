
from __future__ import annotations
from dataclasses import dataclass

from mpl_ascii.scene.fingerprint import Fingerprintable, f8
from mpl_ascii.scene.geometry.point import Point2d


@dataclass(frozen=True)
class Matrix2d(Fingerprintable):
    a: float
    b: float
    c: float
    d: float

    def __mul__(self, p: Point2d) -> Point2d:

        x_new = self.a * p.x + self.b * p.y
        y_new = self.c * p.x + self.d * p.y

        return Point2d(x_new, y_new)

    def __matmul__(self, other: Matrix2d) -> Matrix2d:
        new_a = self.a * other.a + self.b * other.c
        new_b = self.a * other.b + self.b * other.d
        new_c = self.c * other.a + self.d * other.c
        new_d = self.c * other.b + self.d * other.d
        return Matrix2d(new_a, new_b, new_c, new_d)

    def __repr__(self) -> str:
        row1 = f"| {self.a:4.3f}  {self.b:4.3f} |"
        row2 = f"| {self.c:4.3f}  {self.d:4.3f} |"
        return f"{row1}\n{row2}"


    def det(self) -> float:
        return self.a * self.d - self.b * self.c


    def inverse(self) -> Matrix2d:
        det = self.det()
        if det == 0:
            raise ValueError(f"Matrix {self} is not invertible (determinant is 0).")
        inv_det = 1.0 / det
        return Matrix2d(
            self.d * inv_det,  -self.b * inv_det,
            -self.c * inv_det,  self.a * inv_det
        )

    def fingerprint(self) -> bytes:
        return f"M({f8(self.a)},{f8(self.b)},{f8(self.c)},{f8(self.d)})".encode()