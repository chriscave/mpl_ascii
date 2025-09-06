from __future__ import annotations
from dataclasses import dataclass
from typing import Union


from mpl_ascii.layout.layout_shape import Edge, ShapeLayout, Vertex
from mpl_ascii.presentation.color_policy import DisplayColors
from mpl_ascii.presentation.visibility import Visibility
from mpl_ascii.layout.render_plan import CharMap
from mpl_ascii.layout.discrete_point import DiscretePoint
from mpl_ascii.scene.entities import ParsedColor, ParsedShape



@dataclass
class Glyph:
    char: str
    color: Union[str, None]

    @classmethod
    def blank(cls):
        return cls(" ", None)

    def __str__(self) -> str:
        return self.char

    def __rich__(self) -> str:
        if self.color:
            return f"[{self.color}]{self.char}[/{self.color}]"
        return self.char


@dataclass
class PointGlyph:
    p: DiscretePoint
    glyph: Glyph


def resolve_glyphs(
        parsed_shape: ParsedShape,
        visible: Visibility,
        display_colors: DisplayColors,
        char_map: CharMap,
        shape_layout: ShapeLayout,
    )-> dict[str, Glyph]:

    def is_white(c: Union[ParsedColor, None]) -> bool:
        if c is None:
            return False
        eps: float = 1e-3
        return c.red > 1-eps and c.green > 1-eps and c.blue > 1-eps

    visible_parsed_pms = [pm for pm in parsed_shape.points if Vertex.id_from_point_mark(pm) in visible.points]
    res: dict[str, Glyph] = {}
    for pm in visible_parsed_pms:
        ident = Vertex.id_from_point_mark(pm)
        hex_point_color = display_colors.point_colors.get(ident)
        if pm.override:
            res[ident] = Glyph(pm.override, hex_point_color)
            continue

        if hex_point_color:
            if is_white(parsed_shape.style_context.point_color):
                res[ident] = Glyph.blank()

            else:
                point_char = char_map.resolve_char(hex_point_color)
                res[ident] = Glyph(point_char, hex_point_color)


    visible_parsed_lms = [lm for lm in parsed_shape.lines if Edge.id_from_line_mark(lm) in visible.edges]
    hex_edge_color = display_colors.line_color
    for lm in visible_parsed_lms:
        ident = Edge.id_from_line_mark(lm)
        if lm.override:
            res[ident] = Glyph(lm.override, hex_edge_color)
            continue

        if hex_edge_color:
            if is_white(parsed_shape.style_context.line_color):
                res[ident] = Glyph.blank()
            else:
                line_char = char_map.resolve_char(hex_edge_color)
                res[ident] = Glyph(line_char, hex_edge_color)

    hex_fill_color = display_colors.fill_color
    if visible.fill:
        fill_points = shape_layout.get_all_fill()
        fill_idents = [fp.id for fp in fill_points]

        if is_white(parsed_shape.style_context.fill_color):
            res.update({ident: Glyph.blank() for ident in fill_idents})

        elif hex_fill_color:
            fill_char = char_map.resolve_char(hex_fill_color)
            res.update({ident: Glyph(fill_char, hex_fill_color) for ident in fill_idents})

    return res
