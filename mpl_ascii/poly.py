from matplotlib.collections import LineCollection, PolyCollection

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color import std_color
from mpl_ascii.line import draw_line, get_errorbars
from mpl_ascii.tools import get_xrange, get_yrange


class ViolinPlots:
    def __init__(self, ax) -> None:
        self.ax = ax
    def update(self, canvas, color_to_ascii):
        return add_violin_plots(canvas, self.ax, color_to_ascii)

def get_violin_plots(ax):
    poly_collection = []
    line_collection = []

    _, error_barlinescols = get_errorbars(ax)


    for collection in ax.collections:
        if isinstance(collection, PolyCollection):
            poly_collection.append(collection)

        if isinstance(collection, LineCollection):
            if collection in error_barlinescols:
                continue
            line_collection.append(collection)

    return poly_collection, line_collection

def add_violin_plots(canvas, ax, color_to_ascii):
    x_range, y_range = get_xrange(ax), get_yrange(ax)
    pcolls, linecolls = get_violin_plots(ax)
    axes_height, axes_width = canvas.shape
    for collection in pcolls:
        char = color_to_ascii[std_color(collection.get_facecolor())]
        for path in collection.get_paths():
            xy_data = path.vertices
            x_data, y_data = [dat[0] for dat in xy_data], [dat[1] for dat in xy_data]
            line = AsciiCanvas(
                draw_line(
                width=axes_width,
                height=axes_height,
                x_data=x_data,
                y_data=y_data,
                x_range=x_range,
                y_range=y_range,
                char = char,
                )
            )
            canvas = canvas.update(line, (0,0))

    for collection in linecolls:

        for xy in collection.get_segments():
            x_data = [p[0] for p in xy]
            y_data = [p[1] for p in xy]
            char = color_to_ascii[std_color(collection.get_color())]
            line = AsciiCanvas(
                draw_line(
                width=axes_width,
                height=axes_height,
                x_data=x_data,
                y_data=y_data,
                x_range=x_range,
                y_range=y_range,
                char = char,
                )
            )
            canvas = canvas.update(line, (0,0))
    return canvas