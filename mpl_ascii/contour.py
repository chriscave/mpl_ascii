from matplotlib.contour import QuadContourSet

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color import std_color
from mpl_ascii.line import draw_line
from mpl_ascii.tools import get_xrange, get_yrange


class ContourPlots:
    def __init__(self, ax) -> None:
        self.ax = ax
        self.collections = [coll for coll in self.ax.collections if isinstance(coll, QuadContourSet)]

    def colors(self):
        colors = []
        for collection in self.collections:
            for color in collection.get_edgecolor():
                color = std_color(color)
                if color in colors:
                    continue
                colors.append(color)

        return colors



    def update(self, canvas, color_to_ascii):
        x_range, y_range = get_xrange(self.ax), get_yrange(self.ax)
        axes_height, axes_width = canvas.shape
        for collection in self.collections:
            for seg, color in zip(collection.allsegs, collection.get_edgecolor()):
                char = color_to_ascii[std_color(color)]
                for xy_data in seg:

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
        return canvas


def get_contour_plots(ax):
    contour_plots = []
    for collection in ax.collections:
        if isinstance(collection, QuadContourSet):
            contour_plots.append(collection)

    if len(contour_plots) == 0:
        return

    return ContourPlots(ax)
