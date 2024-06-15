import matplotlib
from matplotlib.collections import PathCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color import std_color
from mpl_ascii.format import draw_frame


mpl_version = matplotlib.__version__
mpl_version = tuple(map(int, mpl_version.split(".")))

def add_legend(canvas, legend, color_to_ascii):

    # Add legend
    if legend:
        texts = legend.texts
        if mpl_version >= (3,7,0):
            handles = legend.legend_handles
        else:
            handles = legend.legendHandles

        canvas_legend = AsciiCanvas()
        for handle, text in zip(handles, texts):
            char = " "
            if isinstance(handle, Rectangle):
                char = color_to_ascii[std_color(handle.get_facecolor())]
            if isinstance(handle, Line2D):
                char = color_to_ascii[std_color(handle.get_color())]
            if isinstance(handle, PathCollection):
                color = tuple(handle.get_facecolor()[0])
                char = color_to_ascii[std_color(color)]

            arr = np.array([[char] * 3 + [" "] + list(text.get_text())])
            canvas_legend = canvas_legend.update(AsciiCanvas(arr), (canvas_legend.shape[0], 0))

        title = legend.get_title().get_text() or "Legend"
        title = AsciiCanvas(np.array([list(title)]))
        canvas_legend = canvas_legend.update(title, (-2,0))
        legend_frame = AsciiCanvas(draw_frame(canvas_legend.shape[0]+2, canvas_legend.shape[1]+4))
        canvas_legend = legend_frame.update(canvas_legend, (1,2))

        start_idx = int((canvas.shape[1] / 2) - (canvas_legend.shape[1] / 2))

        canvas = canvas.update(canvas_legend, (canvas.shape[0] + 1, start_idx ))

    return canvas