from typing import Optional
from matplotlib._pylab_helpers import Gcf

from matplotlib.backends.backend_agg import (
    FigureManagerBase,
    FigureCanvasAgg,
)
from matplotlib.figure import Figure

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.ax import AxesPlot, draw_ax, get_plots
from mpl_ascii.color_map import FigureColorMap

from rich.console import Console

AXES_WIDTH = 150
AXES_HEIGHT = 40
ENABLE_COLORS = True

UNRELEASED = False

class FigureCanvasAscii(FigureCanvasAgg):

    def __init__(self, figure: Optional[Figure] = ...) -> None:
        super().__init__(figure)

    def to_txt_with_color(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()
        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        all_axes_plots = []
        for ax in self.figure.axes:
            ax_plot = AxesPlot(ax, axes_height, axes_width)
            all_axes_plots.append(ax_plot)

        fig_color_map = FigureColorMap(all_axes_plots)

        image_canvas = AsciiCanvas()
        for ax_plot in all_axes_plots:
            color_map = fig_color_map(ax_plot)
            ax_plot.draw_canvas(color_map)
            if ax_plot.is_colorbar():
                image_canvas = image_canvas.update(ax_plot.color_canvas, (0, image_canvas.shape[1] + 3))
            else:
                image_canvas = image_canvas.update(ax_plot.color_canvas, (image_canvas.shape[0], 0))

        return image_canvas


    def to_txt(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()
        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        all_axes_plots = []
        for ax in self.figure.axes:
            ax_plot = AxesPlot(ax, axes_height, axes_width)
            all_axes_plots.append(ax_plot)

        fig_color_map = FigureColorMap(all_axes_plots)

        image_canvas = AsciiCanvas()
        for ax_plot in all_axes_plots:
            color_map = fig_color_map(ax_plot)
            ax_plot.draw_canvas(color_map)
            if ax_plot.is_colorbar():
                image_canvas = image_canvas.update(ax_plot.canvas, (0, image_canvas.shape[1] + 3))
            else:
                image_canvas = image_canvas.update(ax_plot.canvas, (image_canvas.shape[0], 0))

        return image_canvas

    def print_txt(self, filename, **kwargs):
        if isinstance(filename, str):
            with open(filename, "w") as f:
                f.write(str(self.to_txt()))
        else:
            filename.write(str(self.to_txt()).encode())

class FigureManagerAscii(FigureManagerBase):
    def __init__(self, canvas, num):
        super().__init__(canvas, num)
        self.canvas = canvas

    def show(self):
        canvas = self.canvas
        canvas.draw()
        console = Console()
        if ENABLE_COLORS:
            fig = canvas.to_txt_with_color()
            console.print(fig, highlight=False)
        else:
            fig = canvas.to_txt()
            print(fig)

FigureCanvasAscii.manager_class = FigureManagerAscii
FigureCanvas = FigureCanvasAscii
FigureManager = FigureManagerAscii
