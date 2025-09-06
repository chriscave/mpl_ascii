from matplotlib.collections import PathCollection
from numpy.typing import NDArray
from itertools import zip_longest

from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import Color, ColorMap, Shape, PointMark

def parse(obj: PathCollection) -> Shape:
    points: NDArray = obj.get_offsets() # type: ignore
    parsed_points: list[PointMark] = []
    facecolors: NDArray = obj.get_facecolor() # type: ignore

    color_map = ColorMap.from_mpl_colormap(obj.get_cmap())
    for p, c in zip_longest(points, facecolors, fillvalue=facecolors[0]):
        point = Point(p[0], p[1])
        mark = PointMark(point, color=Color(*c))
        parsed_points.append(mark)

    return Shape(
        parsed_points,
        [],
        to_mapping(obj.get_offset_transform()),
        point_color=Color(*facecolors[0]),
        line_color=None,
    )


