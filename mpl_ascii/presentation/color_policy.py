from dataclasses import dataclass
from typing import Union

import numpy as np
from mpl_ascii.layout.layout_shape import Vertex
from mpl_ascii.scene.entities import ParsedColor, ParsedColorMap, ParsedShape

@dataclass
class DisplayColors:
    point_colors: dict[str, Union[str, None]]
    line_color: Union[str, None]
    fill_color: Union[str, None]


def filter_unusable(c: Union[ParsedColor, None]) -> Union[ParsedColor, None]:
    res: Union[ParsedColor, None] = c

    if c is None or c.alpha == 0:
        res = None

    return res

def apply_theme_constrast(c: ParsedColor) -> str:

    res: str = c.hex_color
    eps = 1e-3
    if c.red < eps and c.green < eps and c.blue < eps:

        res = ParsedColor.to_hex(1.,1.,1.)

    return res

def qualify_color_for_display(color: Union[ParsedColor, None]) -> Union[str, None]:
    c = filter_unusable(color)
    return None if c is None else apply_theme_constrast(c)


def coalese_color(hex_color: str, color_map: ParsedColorMap) -> str:
    """Coalesce a single hex color using the colormap."""
    linspace: list[float] = np.linspace(0,1,10).tolist()

    x = color_map.approx_inverse(ParsedColor.from_hex(hex_color))
    y = 0
    for y in linspace:
        if y > x:
            break

    return color_map(y).hex_color

def qualify_for_display(parsed_shape: ParsedShape) -> DisplayColors:
    default_display_point_color = qualify_color_for_display(parsed_shape.style_context.point_color)
    display_point_colors: dict[str, Union[str, None]] = {}

    for pm in parsed_shape.points:
        ident = Vertex.id_from_point_mark(pm)
        color = qualify_color_for_display(pm.color) if pm.color else default_display_point_color
        display_point_colors[ident] = color

    # Process line color
    display_line_color = qualify_color_for_display(parsed_shape.style_context.line_color)

    # Process fill color
    display_fill_color = qualify_color_for_display(parsed_shape.style_context.fill_color)

    return DisplayColors(
        display_point_colors,
        display_line_color,
        display_fill_color
    )

