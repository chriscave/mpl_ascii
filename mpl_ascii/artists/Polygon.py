from matplotlib.patches import Polygon

from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import Color, LineMark, PointMark, Shape


def parse(obj: Polygon) -> Shape:


    points = [PointMark(Point(p[0], p[1])) for p in obj.get_xy()]

    lines = [
        LineMark(a.point, b.point) for a,b in zip(points[:-1], points[1:])
    ]

    fill_color = Color(*obj.get_facecolor())
    edge_color = Color(*obj.get_edgecolor())

    return Shape(
        points,
        lines,
        to_mapping(obj.axes.transData),
        point_color=edge_color,
        line_color=edge_color,
        fill=fill_color
    )