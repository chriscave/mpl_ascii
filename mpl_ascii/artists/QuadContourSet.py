from matplotlib.contour import QuadContourSet

from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import Color, LineMark, PointMark, Shape


def parse(obj: QuadContourSet) -> list[Shape]:

    shapes: list[Shape] = []
    for array, color in zip(obj.allsegs, obj.get_edgecolor()):

        if len(array) == 0:
            continue

        for sec in array:

            points = [PointMark(Point(*data)) for data in sec]
            lines = [
                LineMark(a.point, b.point) for a,b in zip(points[:-1], points[1:])
            ]

            shapes.append(
                Shape(points, lines, to_mapping(obj.axes.transData), point_color=Color(*color), line_color=Color(*color))
            )

    return shapes