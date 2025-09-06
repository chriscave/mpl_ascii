from __future__ import annotations
from typing import Union, cast
from matplotlib.collections import PathCollection
from matplotlib.colors import to_rgba
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.transforms import Transform

from mpl_ascii.artists.transform_helpers import AffineMap, Point, get_figure2ascii_transform, to_mapping
from mpl_ascii.artists.types import Color, LineMark, PointMark, Shape, TextElement




def parse(obj: Legend) -> list[Union[Shape, TextElement]]:

    x0, y0, _, _ = obj.get_frame().get_bbox().bounds
    figure2ascii = get_figure2ascii_transform(obj.get_figure())
    figure2display: Transform = obj.get_figure().transFigure # type: ignore
    mapping = cast(AffineMap, to_mapping(figure2display)) @ figure2ascii.inverse()
    mapping = AffineMap(mapping.linear, Point(x0,y0))



    shapes: list[Shape] = []
    texts: list[TextElement] = []

    longest_legend_label = max([len(t.get_text()) for t in obj.get_texts()])
    artist_width = 1
    artist_sep = 1
    left_pad = 0
    right_pad = 1
    top_pad = 1

    height = len(obj.get_texts()) + top_pad
    if obj.get_title().get_text():
        height += 1
    width = max(longest_legend_label + artist_width + artist_sep, len(obj.get_title().get_text())) + left_pad + right_pad


    bl = PointMark(Point(0,0), chr(0x2514)) # └
    br = PointMark(Point(width,0), chr(0x2518)) # ┘
    tl = PointMark(Point(0,height), chr(0x250C)) # ┌
    tr = PointMark(Point(width,height), chr(0x2510)) # ┐


    hline1 = LineMark(bl.point, br.point, chr(0x2500))  # ─ horizontal line
    hline2 = LineMark(tl.point, tr.point, chr(0x2500))  # ─ horizontal line

    vline1 = LineMark(bl.point, tl.point, chr(0x2502))  # │ vertical line
    vline2 = LineMark(br.point, tr.point, chr(0x2502))  # │ vertical line

    background_box = Shape(
        [bl, br, tl, tr],
        [hline1, hline2, vline1, vline2],
        mapping,
        fill=Color(1,1,1,1)
        )
    shapes.append(background_box)

    title = TextElement(
        obj.get_title().get_text(),
        anchor=Point(0, height-top_pad),
        transform=mapping,
        horizontal_alignment="left",
        vertical_alignment="center"
    )
    texts.append(title)

    color = None

    for i, (art, text) in enumerate(zip(reversed(obj.legend_handles), reversed(obj.get_texts()))): # type: ignore
        if isinstance(art, PathCollection):
            color = Color(*art.get_facecolor()[0]) # type: ignore
        if isinstance(art, Rectangle):
            color = Color(*art.get_facecolor()) # type: ignore
        if isinstance(art, Line2D):
            color = Color(*to_rgba(art.get_color()))


        point = Point(1,i+1)
        shape = Shape(
            points = [PointMark(point)],
            lines = [],
            mapping=mapping,
            point_color=color
        )
        text = TextElement(
            text.get_text(),
            anchor=point + Point(1,0),
            transform=mapping,
            horizontal_alignment='left',
            vertical_alignment='center'
        )
        shapes.append(shape)
        texts.append(text)


    return shapes + texts