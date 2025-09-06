from dataclasses import dataclass

from mpl_ascii.layout.layout_shape import Edge, Vertex
from mpl_ascii.presentation.color_policy import DisplayColors
from mpl_ascii.scene.entities import ParsedPointMark, ParsedShape

def is_endpoint(pm: ParsedPointMark, shape: ParsedShape) -> bool:
    return pm.p in [lm.a for lm in shape.lines] + [lm.b for lm in shape.lines]


@dataclass
class Visibility:
    points: list[str]
    edges: list[str]
    fill: bool

def decide_visibility(shape: ParsedShape, display_colors: DisplayColors) -> Visibility:
    draw_points: list[str] = []
    draw_edges: list[str] = []
    draw_fill: bool = False

    lw = shape.style_context.line_width
    for pm in shape.points:
        ident = Vertex.id_from_point_mark(pm)
        point_display_color = display_colors.point_colors.get(ident)
        if lw == 0 and is_endpoint(pm, shape):
            continue
        elif point_display_color is None and pm.override is None:
            continue
        else:
            draw_points.append(ident)

    for lm in shape.lines:
        ident = Edge.id_from_line_mark(lm)
        if lw == 0:
            continue
        elif display_colors.line_color is None and lm.override is None:
            continue
        else:
            draw_edges.append(ident)

    if display_colors.fill_color is not None:
        draw_fill = True

    return Visibility(draw_points, draw_edges, draw_fill)
