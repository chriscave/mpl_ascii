from typing import cast
from matplotlib.patches import Rectangle

from mpl_ascii.artists.transform_helpers import AffineMap, Point, to_mapping
from mpl_ascii.artists.types import Color, LineMark, PointMark, Shape

def parse(obj: Rectangle) -> Shape:

    facecolor = obj.get_facecolor()
    facecolor = Color(*facecolor)
    line_color = Color(*obj.get_edgecolor())
    point_color = Color(*obj.get_edgecolor())


    mapping = cast(AffineMap, to_mapping(obj.get_transform()))

    bl_char = chr(0x2514) # └
    br_char = chr(0x2518) # ┘
    tl_char = chr(0x250C) # ┌
    tr_char = chr(0x2510) # ┐

    if y_axis_is_flipped(mapping):
        bl_char, br_char, tl_char, tr_char = tl_char, tr_char, bl_char, br_char

    if x_axis_is_flipped(mapping):
        bl_char, br_char, tl_char, tr_char = br_char, bl_char, tr_char, tl_char

    bl = PointMark(Point(0,0), bl_char)
    br = PointMark(Point(1,0), br_char)
    tl = PointMark(Point(0,1), tl_char)
    tr = PointMark(Point(1,1), tr_char)


    hline1 = LineMark(bl.point, br.point, chr(0x2500))  # ─ horizontal line
    hline2 = LineMark(tl.point, tr.point, chr(0x2500))  # ─ horizontal line

    vline1 = LineMark(bl.point, tl.point, chr(0x2502))  # │ vertical line
    vline2 = LineMark(br.point, tr.point, chr(0x2502))  # │ vertical line

    if abs(obj.get_angle()) > 1e-3:
        bl = PointMark(Point(0,0))
        br = PointMark(Point(1,0))
        tl = PointMark(Point(0,1))
        tr = PointMark(Point(1,1))

        hline1 = LineMark(bl.point, br.point)
        hline2 = LineMark(tl.point, tr.point)
        vline1 = LineMark(bl.point, tl.point)
        vline2 = LineMark(br.point, tr.point)


    return Shape(
        [bl, br, tl, tr],
        [hline1, hline2, vline1, vline2],
        mapping,
        line_width=obj.get_linewidth(),
        fill=facecolor,
        line_color=line_color,
        point_color=point_color
    )


def y_axis_is_flipped(map: AffineMap):
    return map.linear.d < 0

def x_axis_is_flipped(map: AffineMap):
    return map.linear.a < 0