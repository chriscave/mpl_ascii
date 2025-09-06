from matplotlib.collections import LineCollection
import matplotlib.lines as mlines

from mpl_ascii.artists.types import Shape
from mpl_ascii.artists import Line2D


def parse(obj: LineCollection) -> list[Shape]:

    lw = obj.get_linewidths()
    colors = obj.get_colors()
    T = obj.get_transform()
    shapes: list[Shape] = []
    for i, seg in enumerate(obj.get_segments()):
        (x0, y0), (x1, y1) = seg
        ln = mlines.Line2D([x0, x1], [y0, y1],
                           transform=T,
                           linewidth=lw[i % len(lw)],
                           color=colors[i % len(colors)])
        shapes.append(Line2D.parse(ln))

    return shapes