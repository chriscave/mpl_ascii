from typing import Optional
from matplotlib._pylab_helpers import Gcf

from matplotlib.backends.backend_agg import (
    FigureManagerBase,
    FigureCanvasAgg,
)
from matplotlib.figure import Figure

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.ax import AxesPlot
from mpl_ascii.color_map import FigureColorMap
from mpl_ascii.draw import draw_ax, get_plots

from rich.console import Console

AXES_WIDTH = 150
AXES_HEIGHT = 40
ENABLE_COLORS = True

UNRELEASED = False

def show():
    for manager in Gcf.get_all_fig_managers():
        canvas = manager.canvas
        canvas.draw()
        console = Console()
        if ENABLE_COLORS:
            fig = canvas.to_txt_with_color()
            console.print(fig, highlight=False)
        else:
            fig = canvas.to_txt()
            print(fig)

def draw_figure(axes_plots):
    image_canvas = AsciiCanvas()
    for ax in axes_plots:
        if UNRELEASED:
            if ax.is_colorbar():
                continue
        image_canvas = image_canvas.update(ax.canvas, (image_canvas.shape[0], 0))
        if UNRELEASED:
            if ax.colorbar:
                color_bar = ax.colorbar
                image_canvas = image_canvas.update(color_bar.canvas, (0, image_canvas.shape[1]))

    return image_canvas

class FigureCanvasAscii(FigureCanvasAgg):

    def __init__(self, figure: Optional[Figure] = ...) -> None:
        super().__init__(figure)
        self.fig_color_map = FigureColorMap(figure)


    def get_all_axes_plots(self):
        figure = self.figure
        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        axes_plots = []

        for ax in figure.axes:
            # color_map = self.fig_color_map(ax)
            axes_plot = AxesPlot(ax, axes_height, axes_width)
            axes_plots.append(axes_plot)

        if UNRELEASED:
            colorbars =[ax.is_colorbar() for ax in axes_plots]
            if True in colorbars:
                idx = colorbars.index(True)
                ax_with_color_bar = axes_plots[idx - 1]
                ax_with_color_bar.colorbar = axes_plots[idx]

        self.axes_plots = axes_plots

        return axes_plots


    def to_txt_with_color(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        axes_plots = self.get_all_axes_plots()
        ascii_canvases = [ax_plot.canvas for ax_plot in axes_plots]

        color_ascii_canvases = []
        for canvas, ax in zip(ascii_canvases, self.figure.axes):
            color_map = self.fig_color_map(ax)
            arr = canvas.array
            for color in color_map:
                arr[arr==color_map[color]]=f"[{color}]{color_map[color]}[/{color}]"
            canvas.array = arr
            color_ascii_canvases.append(canvas)

        image_canvas = draw_figure(axes_plots)

        return image_canvas


    def to_txt(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        axes_plots = self.get_all_axes_plots()

        image_canvas = draw_figure(axes_plots)
        return image_canvas


    def print_txt(self, filename, **kwargs):
        if isinstance(filename, str):
            with open(filename, "w") as f:
                f.write(str(self.to_txt()))
        else:
            filename.write(str(self.to_txt()).encode())



FigureCanvas = FigureCanvasAscii
FigureManager = FigureManagerBase
