from __future__ import annotations
from dataclasses import dataclass

from mpl_ascii.scene.geometry.affine import AffineMap2d
from mpl_ascii.scene.geometry.point import Point2d


@dataclass
class TransformableShape:
    points: tuple[Point2d,...]
    lines: tuple[tuple[Point2d, Point2d],...]

    def apply_transform(self, T: AffineMap2d) -> TransformableShape:
        new_points = tuple(T(p) for p in self.points)
        new_lines = tuple((T(l[0]), T(l[1])) for l in self.lines)
        return TransformableShape(new_points, new_lines)
