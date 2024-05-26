from matplotlib.collections import QuadMesh

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.bar import draw_bar
from mpl_ascii.color import std_color
from mpl_ascii.tools import linear_transform, get_yrange


class ColorbarPlot:
    def __init__(self, ax) -> None:
        self.ax = ax
        self.colorbar = get_colorbar(ax)
        self.tick_data = [tick.get_loc() for tick in self.ax.yaxis.get_major_ticks()]
        self.cmap = self.colorbar.cmap
        self.norm = self.colorbar.norm

    def update(self, canvas: AsciiCanvas, color_to_ascii) -> AsciiCanvas:
        return add_colorbar(self.ax, canvas, color_to_ascii)


def get_colorbar(ax):
    colorbar = None
    for collection in ax.collections:
        if isinstance(collection, QuadMesh):
            colorbar = collection

    return colorbar

def add_colorbar(ax, canvas, color_to_ascii):
    colorbar = get_colorbar(ax)
    axes_height, axes_width = canvas.shape
    y_range = get_yrange(ax)

    color_bar_width = axes_width

    tick_data = [tick.get_loc() for tick in ax.yaxis.get_major_ticks()]
    for i in range(1, len(tick_data)):
        top_value = tick_data[i]
        bottom_value = tick_data[i-1]
        if tick_data[i] > y_range[1]:
            top_value = y_range[1]
        top = round(linear_transform(top_value, y_range[0], y_range[1], 1, axes_height))
        bottom = round(linear_transform(bottom_value, y_range[0], y_range[1], 1, axes_height))
        cmap, norm = colorbar.cmap, colorbar.norm
        char = color_to_ascii[std_color(cmap(norm(top_value)))]
        bar_height = top - bottom
        if i == 1:
            bar_height = top

        c = AsciiCanvas(draw_bar(
            bar_height,
            color_bar_width,
            axes_height,
            color_bar_width,
            (0,color_bar_width-1),
            (1,axes_height),
            char
        ))

        canvas = canvas.update(c, (axes_height - top, 0))

    return canvas