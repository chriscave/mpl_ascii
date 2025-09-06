from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon

from mpl_ascii.artists.Polygon import parse as parse_polygon
from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import Color, LineMark, PointMark, Shape

def parse(obj: PolyCollection):
    paths = obj.get_paths()
    shapes: list[Shape] = []



    for p in paths:

        points = [PointMark(Point(p[0], p[1])) for p in p.vertices]


        lines = [
            LineMark(a.point, b.point) for a,b in zip(points[:-1], points[1:])
        ]

        facecolor = Color(*obj.get_facecolor()[0]) if len(obj.get_facecolor()) > 0 else None
        # edgecolor = Color(*obj.get_edgecolor()[0]) if len(obj.get_edgecolor()) > 0 else None

        shapes.append(
            Shape(
                points,
                lines,
                to_mapping(obj.axes.transData),
                point_color=facecolor,
                line_color=facecolor,
                fill=facecolor
        ))

    return shapes
