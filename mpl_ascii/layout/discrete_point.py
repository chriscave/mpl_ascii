from __future__ import annotations
from dataclasses import dataclass

from mpl_ascii.scene.geometry.point import Point2d


@dataclass(frozen=True)
class DiscretePoint:
    x: int
    y: int

    @classmethod
    def from_point2d(cls, p: Point2d) -> DiscretePoint:
        return cls(int(round(p.x)), int(round(p.y)))

    def get_row_column_coords(self, height: int, width: int) -> tuple[int, int]:
        row = height - self.y - 1
        column = self.x

        return row, column

    def __add__(self, other: DiscretePoint) -> DiscretePoint:
        return DiscretePoint(self.x + other.x, self.y + other.y)


    def __repr__(self) -> str:
        return f"{self.x, self.y}"

