from matplotlib._pylab_helpers import Gcf

from matplotlib.backends.backend_agg import (
    FigureManagerBase,
    RendererAgg,
    FigureCanvasAgg,
)
from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color_map import map_color_to_ascii
from mpl_ascii.draw import draw_bar, draw_frame, draw_line, draw_x_ticks, draw_y_ticks
from mpl_ascii.tools import linear_transform

AXES_WIDTH = 150
AXES_HEIGHT = 40

class RendererAscii(RendererAgg):

    def __init__(self, width, height, dpi):
        super(RendererAscii, self).__init__(width, height, dpi)
        self.texts = []
        self.tick_info = []

    def clear(self):
        super(RendererAscii, self).clear()
        self.texts = []
        self.tick_info = []

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        super(RendererAscii, self).draw_text(
            gc, x, y, s, prop, angle, ismath=ismath, mtext=mtext
        )

        if mtext is not None:
            self.texts.append(mtext)


def show():
    for manager in Gcf.get_all_fig_managers():
        canvas = manager.canvas
        canvas.draw()
        string = canvas.to_txt()
        print(string)


class FigureCanvasAscii(FigureCanvasAgg):

    def __init__(self, figure: Figure | None = ...) -> None:
        super().__init__(figure)
        self.tick_info = []

    def get_renderer(self):
        w, h = self.figure.bbox.size
        key = w, h, self.figure.dpi
        reuse_renderer = self._lastKey == key
        if not reuse_renderer:
            self.renderer = RendererAscii(w, h, self.figure.dpi)
            self._lastKey = key
        return self.renderer

    def to_txt(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        figure = self.figure

        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        frame_buffer_left = 1
        frame_buffer_right = 1
        frame_buffer_top = 1
        frame_buffer_bottom = 1


        frame_width = axes_width + frame_buffer_left + frame_buffer_right
        frame_height = axes_height + frame_buffer_top + frame_buffer_bottom

        ascii_canvases = []
        for ax in figure.axes:
            color_to_ascii = map_color_to_ascii(ax)

            x_range = ax.get_xlim()
            if x_range[1] < x_range[0]:
                x_range = x_range[1], x_range[0]

            y_range = ax.get_ylim()
            if y_range[1] < y_range[0]:
                y_range = y_range[1], y_range[0]

            x_min, x_max = x_range
            y_min, y_max = y_range

    def to_txt(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        figure = self.figure
        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        ascii_canvases = []
        for ax in figure.axes:
            canvas = draw_ax(ax, axes_height, axes_width)
            ascii_canvases.append(canvas)

        image_canvas = AsciiCanvas()
        for canvas in ascii_canvases:
            image_canvas = image_canvas.update(canvas, (image_canvas.shape[0], 0))

        return str(image_canvas)


    def print_txt(self, filename, **kwargs):
        if isinstance(filename, str):
            with open(filename, "w") as f:
                f.write(self.to_txt())
        else:
            filename.write(self.to_txt().encode())


FigureCanvas = FigureCanvasAscii
FigureManager = FigureManagerBase
