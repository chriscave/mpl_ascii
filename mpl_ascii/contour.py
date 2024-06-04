import matplotlib
from matplotlib.collections import PathCollection
from matplotlib.contour import QuadContourSet

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color import std_color
from mpl_ascii.line import draw_line
from mpl_ascii.tools import get_xrange, get_yrange

mpl_version = matplotlib.__version__
mpl_version = tuple(map(int, mpl_version.split(".")))


class ContourPlots:
    def __init__(self, ax) -> None:
        self.ax = ax
        self.collections = []
        if mpl_version >= (3,8,0):
            self.collections = [coll for coll in self.ax.collections if isinstance(coll, QuadContourSet)]
        else:
            for pc in ax.collections:
                if isinstance(pc, PathCollection):
                    paths = pc.get_paths()
                    sizes = pc.get_sizes()
                    if len(paths) > 0 and len(sizes) == 0:
                        self.collections.append(pc)


        self._colors = []
        for collection in self.collections:
            if mpl_version >= (3,8,0):
                for seg, color in zip(collection.allsegs, collection.get_edgecolor()):
                    if len(seg) == 0:
                        continue
                    color = std_color(color)
                    if color in self._colors:
                        continue
                    self._colors.append(color)

            else:
                for color in collection.get_edgecolor():
                    color = std_color(color)
                    if color in self._colors:
                        continue
                    self._colors.append(color)

        self._colors = sorted(self._colors)

    @property
    def colors(self):
        return self._colors

    def update(self, canvas, color_to_ascii):
        x_range, y_range = get_xrange(self.ax), get_yrange(self.ax)
        axes_height, axes_width = canvas.shape
        if mpl_version >= (3,8,0):

            for collection in self.collections:
                for seg, color in zip(collection.allsegs, collection.get_edgecolor()):
                    if len(seg) == 0:
                        continue
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

        else:
            for collection in self.collections:
                color = collection.get_edgecolor()[0]
                for path in collection.get_paths():
                    char = color_to_ascii[std_color(color)]
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
            return canvas

def get_contour_plots(ax):
    if mpl_version >= (3,8,0):
        for collection in ax.collections:
            if isinstance(collection, QuadContourSet):
                return ContourPlots(ax)

    else:
        for pc in ax.collections:
            if isinstance(pc, PathCollection):
                paths = pc.get_paths()
                sizes = pc.get_sizes()
                if len(paths) > 0 and len(sizes) == 0:
                    return ContourPlots(ax)

    return None
