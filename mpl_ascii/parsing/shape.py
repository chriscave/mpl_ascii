from __future__ import annotations
from mpl_ascii.artists.types import Color, LineMark, Point, PointMark, Shape, TextElement
from mpl_ascii.scene.geometry.point import Point2d
from mpl_ascii.parsing.transform import parse_mapping
from mpl_ascii.scene.entities import ParsedColor, ParsedLineMark, ParsedPointMark, ParsedShape, ParsedText, StyleContext


def parse_point(p: Point) -> Point2d:
    return Point2d(p.x, p.y)

def parse_line(line: tuple[Point, Point]) -> tuple[Point2d, Point2d]:
    return (parse_point(line[0]), parse_point(line[1]))

def parse_point_mark(pm: PointMark) -> ParsedPointMark:
    color = parse_color(pm.color) if pm.color else None
    return ParsedPointMark(parse_point(pm.point), pm.char_override, color)

def parse_line_mark(lm: LineMark) -> ParsedLineMark:
    return ParsedLineMark(parse_point(lm.a), parse_point(lm.b), lm.char_override)

def parse_shape(shape: Shape, zorder: float, insert_order: float) -> ParsedShape:

    point_color = parse_color(shape.point_color) if shape.point_color else None
    line_color = parse_color(shape.line_color) if shape.line_color else None
    fill_color = parse_color(shape.fill) if shape.fill else None


    return ParsedShape(
        tuple(parse_point_mark(p) for p in shape.points),
        tuple(parse_line_mark(l) for l in shape.lines),
        StyleContext(
            point_color,
            line_color,
            fill_color,
            line_width=shape.line_width,
        ),
        zorder=shape.override_zorder or zorder,
        transform2display=parse_mapping(shape.mapping),
        insert_order=insert_order
    )

def parse_color(color: Color) -> ParsedColor:
    return ParsedColor(
        color.red,
        color.green,
        color.blue,
        color.alpha,
    )

def parse_text(text_elmt: TextElement, zorder: float, insert_order: float) -> ParsedText:
    return ParsedText(
        text=text_elmt.text,
        anchor=parse_point(text_elmt.anchor),
        orientation=text_elmt.orientation,
        horizontal_alignment=text_elmt.horizontal_alignment,
        vertical_alignment=text_elmt.vertical_alignment,
        zorder=zorder,
        transform2display=parse_mapping(text_elmt.transform),
        insert_order=insert_order
    )
