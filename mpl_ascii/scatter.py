from itertools import zip_longest
from matplotlib.collections import PathCollection
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color import Char, std_color
from mpl_ascii.tools import linear_transform, get_xrange, get_yrange


class ScatterPlot:
    def __init__(self, ax) -> None:
        self.ax = ax
        self.scatter_plots = get_scatter_plots(self.ax)
        self.values = [coll.get_array() for coll in self.scatter_plots]
        self.colors = [coll.get_facecolor() for coll in self.scatter_plots]


    def update(self, canvas, color_to_ascii):
        return add_scatter_plots(canvas, self.ax, color_to_ascii)


def get_scatter_plots(ax):
    scatter_plots = []
    for collection in ax.collections:
        if isinstance(collection, PathCollection):
            paths = collection.get_paths()
            sizes = collection.get_sizes()
            if len(paths) > 0 and len(sizes) > 0:
                scatter_plots.append(collection)

    return scatter_plots


def add_scatter_plots(canvas, ax, color_to_ascii):
    x_range, y_range = get_xrange(ax), get_yrange(ax)
    axes_height, axes_width = canvas.shape
    x_min, x_max = x_range
    y_min, y_max = y_range

    for collection in get_scatter_plots(ax):
        offsets = collection.get_offsets()
        if len(collection.get_facecolor()) > 0:
            default_color = collection.get_facecolor()[0]
            colors = collection.get_facecolor()

        if len(collection.get_edgecolor()) > 0:
            default_color = collection.get_edgecolor()[0]
            colors = collection.get_edgecolor()


        for point,color in zip_longest(offsets, colors, fillvalue=default_color):
            color = tuple(color)

            x_new = round(linear_transform(point[0], x_min, x_max, 0, axes_width-1))
            y_new = round(linear_transform(point[1], y_min, y_max, 1, axes_height))

            char = color_to_ascii.get(std_color(color), Char("+", "white"))
            canvas = canvas.update(AsciiCanvas(np.array([[char]])), (axes_height-y_new, x_new))

    return canvas