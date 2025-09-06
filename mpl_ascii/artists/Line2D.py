from typing import cast
from matplotlib.colors import to_rgba
from matplotlib.lines import Line2D

from mpl_ascii.artists.transform_helpers import AffineMap, Point, to_mapping
from mpl_ascii.artists.types import LineMark, PointMark, Shape, Color


def parse(obj: Line2D) -> Shape:
    x_data = obj.get_xdata()
    y_data = obj.get_ydata()

    color = to_rgba(obj.get_color()) # type: ignore


    points = [
        PointMark(Point(x,y)) for x,y in zip(x_data, y_data)
    ]
    lines = [
        LineMark(a.point, b.point) for a,b in zip(points[:-1], points[1:])
    ]

    return Shape(
        points=points,
        lines=lines,
        mapping=to_mapping(obj.get_transform()),
        point_color=Color(*color),
        line_color=Color(*color),
    )