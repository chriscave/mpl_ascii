from matplotlib._pylab_helpers import Gcf

from matplotlib.backends.backend_agg import (
    FigureManagerBase,
    RendererAgg,
    FigureCanvasAgg,
)
from matplotlib.figure import Figure

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color_map import Char, ax_color_map
from mpl_ascii.draw import draw_ax

from rich.console import Console

AXES_WIDTH = 150
AXES_HEIGHT = 40
ENABLE_COLORS = True

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
        console = Console()
        if ENABLE_COLORS:
            fig = canvas.to_txt_with_color()
            console.print(fig, highlight=False)
        else:
            fig = canvas.to_txt()
            print(fig)



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

    def to_txt_with_color(self, sep="\n", tw=240, invert=False, threshold=200):
        self.draw()

        figure = self.figure
        axes_height = AXES_HEIGHT
        axes_width = AXES_WIDTH

        ascii_canvases = []
        for ax in figure.axes:
            canvas = draw_ax(ax, axes_height, axes_width)
            color_map = ax_color_map(ax)
            arr = canvas.array
            for color in color_map:
                arr[arr==color_map[color]]=f"[{color}]{color_map[color]}[/{color}]"
            canvas.array = arr
            ascii_canvases.append(canvas)

        image_canvas = AsciiCanvas()
        for canvas in ascii_canvases:
            image_canvas = image_canvas.update(canvas, (image_canvas.shape[0], 0))

        return image_canvas


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

        return image_canvas


    def print_txt(self, filename, **kwargs):
        if isinstance(filename, str):
            with open(filename, "w") as f:
                f.write(str(self.to_txt()))
        else:
            filename.write(str(self.to_txt()).encode())


FigureCanvas = FigureCanvasAscii
FigureManager = FigureManagerBase
