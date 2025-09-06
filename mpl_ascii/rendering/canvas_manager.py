import io
from typing import Union
from matplotlib.backend_bases import FigureCanvasBase, FigureManagerBase
from matplotlib.figure import Figure

from mpl_ascii.rendering.canvas import AsciiCanvas
from mpl_ascii.artists.transform_helpers import AffineMap, Matrix
from mpl_ascii.artists.types import Point
from mpl_ascii.parsing.figure import from_figure
from mpl_ascii.rendering.render import draw_figure
from mpl_ascii.scene.store import Store

from matplotlib.backends.backend_agg import FigureCanvasAgg



class FigureCanvasAscii(FigureCanvasBase):
    def __init__(self, figure: Figure) -> None:
        super().__init__(figure)
        self.figure_canvas: Figure = figure


    def force_draw(self):
        # This forces a draw of the figure. It ensures that locations that are set automatically by matplotlib are updated.
        # Some examples of this are:
        # - tick locations
        # - legend location
        ascii_canvas = self.figure_canvas.canvas
        try:
            FigureCanvasAgg(self.figure_canvas)
            self.figure_canvas.canvas.draw() # type: ignore
        finally:
            self.figure_canvas.set_canvas(ascii_canvas)



    def draw_canvas(self) -> AsciiCanvas:

        self.force_draw()
        width, height = self.get_canvas_width_height()
        M = Matrix(width-1, 0,0,height-1)
        figure2ascii_canvas_transform = AffineMap(M, Point(0,0))
        self.figure2ascii_canvas_transform = figure2ascii_canvas_transform

        store = Store.empty()
        parsed_figure = from_figure(self.figure_canvas, store)
        store.add(parsed_figure)

        canvas = draw_figure(parsed_figure, height, width, store)

        return canvas

    def get_canvas_width_height(self) -> tuple[int, int]:
        width_in, height_in = self.figure_canvas.get_size_inches() # type: ignore


        ascii_char_width_height_ratio = 1.8

        scale = 12

        chars_per_inch_x = 1 * scale
        chars_per_inch_y = chars_per_inch_x / ascii_char_width_height_ratio

        ascii_canvas_width = int(width_in * chars_per_inch_x)
        ascii_canvas_height = int(height_in * chars_per_inch_y)

        return ascii_canvas_width, ascii_canvas_height

    def print_txt(self, writable: Union[str, io.BytesIO], **kwargs):

        if isinstance(writable, str):
            with open(writable, "w") as f:
                f.write(str(self.draw_canvas()))
        else:
            writable.write(str(self.draw_canvas()).encode())


class FigureManagerAscii(FigureManagerBase):
    def __init__(self, canvas: FigureCanvasAscii, num: Union[int, str]):
        super().__init__(canvas, num)

        self.ascii_canvas: FigureCanvasAscii = canvas

    def show(self) -> None:

        canvas = self.ascii_canvas.draw_canvas()

        ENABLE_COLORS = True
        if ENABLE_COLORS == True:
            from rich.console import Console
            console = Console()
            console.print(canvas, highlight=False)

        else:
            print(canvas)
