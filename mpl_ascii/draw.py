import matplotlib
from matplotlib.contour import QuadContourSet
from matplotlib.text import Annotation, Text
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.line import draw_line
from mpl_ascii.tools import linear_transform


mpl_version = matplotlib.__version__
mpl_version = tuple(map(int, mpl_version.split(".")))



def add_contours(canvas, collections, axes_height, axes_width, x_range, y_range, color_to_ascii):
    for collection in collections:
        if isinstance(collection, QuadContourSet):
            for seg in collection.allsegs:
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
                            char = "-",
                        )
                    )
                    canvas = canvas.update(line, (0,0))

    return canvas


def add_text(canvas, texts, axes_height, axes_width, x_range, y_range):
    x_min, x_max = x_range
    y_min, y_max = y_range

    for text in texts:
        if isinstance(text, Annotation):
            continue
        if isinstance(text, Text):
            text_xy = text.get_position()
            text_canvas = AsciiCanvas(np.array([list(text.get_text())]))
            ascii_x = round(linear_transform(text_xy[0], x_min, x_max, 0, axes_width-1))
            ascii_y = round(linear_transform(text_xy[1], y_min, y_max, 1, axes_height))
            canvas = canvas.update(text_canvas, (axes_height - ascii_y, ascii_x))

    return canvas
