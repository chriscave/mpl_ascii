from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from matplotlib.figure import Figure
from matplotlib.transforms import Transform


@dataclass
class Point:
    x: float
    y: float

    def __repr__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"

    def __add__ (self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


def get_figure2ascii_transform(fig: Figure) -> AffineMap:
    return fig.canvas.figure2ascii_canvas_transform # type: ignore


def to_mapping(transform: Transform) -> Mapping:

    affine = transform.get_affine() # type: ignore

    if affine is not None:
        M: NDArray[np.float64] = affine.get_matrix()  # type: ignore
        mat = Matrix(M[0,0], M[0,1], M[1,0], M[1,1]) # type: ignore
        t = AffineMap(mat, Point(M[0,2], M[1,2])) # type: ignore
        return t

    else:
        raise Exception("Expected Affine2D transform")


def blend_affine_maps(x_mapping: AffineMap, y_mapping: AffineMap) -> AffineMap:

    A_x = x_mapping.linear
    if not A_x.b == 0:
        raise Exception(f"Can not blend because {x_mapping} depends on y coordinates")

    A_y = y_mapping.linear
    if not A_y.c == 0:
        raise Exception(f"Can not blend because {y_mapping} depends on x coordinates")

    new_A = Matrix(A_x.a, 0, 0, A_y.d)
    new_b = Point(x_mapping.translation.x, y_mapping.translation.y)

    return AffineMap(new_A, new_b)

@dataclass(frozen=True)
class Matrix:
    a: float
    b: float
    c: float
    d: float

    def __mul__(self, p: Point) -> Point:

        x_new = self.a * p.x + self.b * p.y
        y_new = self.c * p.x + self.d * p.y

        return Point(x_new, y_new)

    def __matmul__(self, other: Matrix) -> Matrix:
        new_a = self.a * other.a + self.b * other.c
        new_b = self.a * other.b + self.b * other.d
        new_c = self.c * other.a + self.d * other.c
        new_d = self.c * other.b + self.d * other.d
        return Matrix(new_a, new_b, new_c, new_d)

    def __repr__(self) -> str:
        row1 = f"| {self.a:4.3f}  {self.b:4.3f} |"
        row2 = f"| {self.c:4.3f}  {self.d:4.3f} |"
        return f"{row1}\n{row2}"


    def det(self) -> float:
        return self.a * self.d - self.b * self.c


    def inverse(self) -> Matrix:
        det = self.det()
        if det == 0:
            raise ValueError(f"Matrix {self} is not invertible (determinant is 0).")
        inv_det = 1.0 / det
        return Matrix(
            self.d * inv_det,  -self.b * inv_det,
            -self.c * inv_det,  self.a * inv_det
        )

class Mapping(ABC):

    def __call__(self, point: Point) -> Point:
        raise NotImplementedError()


@dataclass(frozen=True)
class AffineMap(Mapping):
    linear: Matrix
    translation: Point

    def inverse(self) -> AffineMap:
        A_inv = self.linear.inverse()
        Ab = A_inv * self.translation
        b_inv = Point(-Ab.x, -Ab.y)
        return AffineMap(A_inv, b_inv)

    def __call__(self, other: Point) -> Point:
        return self.linear * other + self.translation

    def __matmul__(self, other: AffineMap) -> AffineMap:
        new_A = self.linear @ other.linear
        new_b = self.linear * other.translation + self.translation
        return AffineMap(new_A, new_b)

    def __repr__(self) -> str:
        row1 = f"| {self.linear.a:4.3f}  {self.linear.b:4.3f} | + | {self.translation.x:4.3f} |"
        row2 = f"| {self.linear.c:4.3f}  {self.linear.d:4.3f} |   | {self.translation.y:4.3f} |"
        return f"{row1}\n{row2}"

    def translate(self, point: Point) -> AffineMap:
        return AffineMap(self.linear, self.translation + point)

    @classmethod
    def identity(cls):
        A = Matrix(1,0,0,1)
        b = Point(0,0)
        return cls(A, b)