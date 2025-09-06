from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Literal, Union

from matplotlib.colors import Colormap


from mpl_ascii.artists.transform_helpers import Mapping, Point



@dataclass
class PointMark:
    point: Point
    char_override: Union[str, None] = None
    color: Union[Color, None] = None

@dataclass
class LineMark:
    a: Point
    b: Point
    char_override: Union[str, None] = None


@dataclass
class ColorMap:
    _call: Callable[[float], Color]

    @classmethod
    def from_mpl_colormap(cls, cmap: Colormap) -> ColorMap:
        def call(x: float):
            return Color(*cmap(x))
        return cls(call)

    def __call__(self, x: float) -> Color:
        return self._call(x)



@dataclass
class Shape:
    points: list[PointMark]
    lines: list[LineMark]
    mapping: Mapping
    line_width: Union[float, None] = None
    point_color: Union[Color, None] = None
    line_color: Union[Color, None] = None
    fill: Union[Color, None] = None
    override_zorder: Union[float, None] = None

@dataclass
class TextElement:
    text: str
    anchor: Point
    transform: Mapping
    horizontal_alignment: Literal["left", "center", "right"]
    vertical_alignment: Literal["top", "center_baseline", "center", "baseline", "bottom"]
    orientation: Literal["horizontal", "vertical"] = "horizontal"

@dataclass
class Color:
    red: float
    green: float
    blue: float
    alpha: float

