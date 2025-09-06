from __future__ import annotations
from dataclasses import dataclass

from abc import ABC, abstractmethod


from mpl_ascii.presentation.glyphs import Glyph, PointGlyph
from mpl_ascii.layout.discrete_point import DiscretePoint


class Renderable(ABC):
    @abstractmethod
    def render(self, canvas: AsciiCanvas) -> AsciiCanvas:
        pass


@dataclass
class RenderableElement(Renderable):
    points: list[PointGlyph]


    def render(self, canvas: AsciiCanvas) -> AsciiCanvas:
        for p in self.points:
            canvas.add(p.p, p.glyph)

        return canvas
@dataclass
class AsciiCanvas:
    height: int
    width: int
    array: list[list[Glyph]]

    @classmethod
    def initialise(cls, height:int, width:int):
        blank_array = [[Glyph.blank() for _ in range(width)] for _ in range(height)]
        return cls(height, width, blank_array)

    def add(self, point: DiscretePoint, glyph: Glyph) -> AsciiCanvas:
        r, c = point.get_row_column_coords(self.height, self.width)
        self.array[r][c] = glyph
        return self


    def __str__(self) -> str:
        res: list[str] = []
        for row in self.array:
            res.append("".join([str(glyph) for glyph in row]))

        return "\n".join(res)

    def __rich__(self) -> str:
        res: list[str] = []
        for row in self.array:
            res.append("".join([glyph.__rich__() for glyph in row]))

        return "\n".join(res)


