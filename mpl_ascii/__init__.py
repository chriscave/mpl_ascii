from typing import Optional
from matplotlib._pylab_helpers import Gcf

from matplotlib.backends.backend_agg import (
    FigureManagerBase,
    FigureCanvasAgg,
)
from matplotlib.figure import Figure

from mpl_ascii.ascii_canvas import AsciiCanvas
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



class FigureCanvasAscii(FigureCanvasAgg):

    def __init__(self, figure: Optional[Figure] = ...) -> None:
        super().__init__(figure)
        self.fig_color_map = FigureColorMap(figure)

    def draw_all_axes(self):
        figure = self.figure
        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        ascii_canvases = []
        all_ax_plots = []
        for ax in figure.axes:
            all_ax_plots.append(get_plots(ax))

        for ax, all_plots in zip(figure.axes, all_ax_plots):
            color_map = self.fig_color_map(ax)
            canvas = draw_ax(ax, all_plots, axes_height, axes_width, color_map)
            ascii_canvases.append(canvas)

        return ascii_canvases

    def to_txt_with_color(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        ascii_canvases = self.draw_all_axes()

        color_ascii_canvases = []
        for canvas, ax in zip(ascii_canvases, self.figure.axes):
            color_map = self.fig_color_map(ax)
            arr = canvas.array
            for color in color_map:
                arr[arr==color_map[color]]=f"[{color}]{color_map[color]}[/{color}]"
            canvas.array = arr
            color_ascii_canvases.append(canvas)

        image_canvas = AsciiCanvas()
        for canvas in color_ascii_canvases:
            image_canvas = image_canvas.update(canvas, (image_canvas.shape[0], 0))

        # for ax in list_of_axes:
        #     if ax.is_colorbar:
        #         continue
        #     image_canvas = image_canvas.update(ax.canvas, (image_canvas.shape[0], 0))
        #     if ax.has_associated_cb:
        #         image_canvas = image_canvas.update(ax.canvas, (0, image_canvas.shape[1]))

        return image_canvas


    def to_txt(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        ascii_canvases = self.draw_all_axes()

        image_canvas = AsciiCanvas()
        for canvas in ascii_canvases:
            image_canvas = image_canvas.update(canvas, (image_canvas.shape[0], 0))

        return image_canvas


    def print_txt(self, filename, **kwargs):
        if isinstance(filename, str):
            with open(filename, "w") as f:
                f.write(str(self.to_txt()))
        else:
            filename.write(str(self.to_txt()).encode())


FigureCanvas = FigureCanvasAscii
FigureManager = FigureManagerBase
