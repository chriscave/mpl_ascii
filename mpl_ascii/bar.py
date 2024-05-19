from matplotlib.container import BarContainer
from matplotlib.patches import Rectangle
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas

from mpl_ascii.color import std_color
from mpl_ascii.tools import linear_transform, scale_factor


def get_bars(ax):
    bars = []
    for container in ax.containers:
        # Draw Bar chart
        if not isinstance(container, BarContainer):
            continue
        for bar in container.patches:
            if not isinstance(bar, Rectangle):
                continue
            bars.append(bar)

    return bars

def draw_bar(bar_height, bar_width, ax_height, ax_width, x_range, y_range, char):
    x_min, x_max = x_range[0], x_range[1]
    y_min, y_max = y_range[0], y_range[1]

    ascii_width_bar = round(bar_width * scale_factor(x_min, x_max, 0, ax_width-1))
    ascii_height_bar = round(bar_height * scale_factor(y_min, y_max, 1, ax_height))

    return np.full((ascii_height_bar, ascii_width_bar), fill_value=char)

def add_bar_chart(canvas, ax, x_range, y_range, color_to_ascii):
    axes_height, axes_width = canvas.shape
    x_min, x_max = x_range
    y_min, y_max = y_range

    bars = get_bars(ax)
    for bar in bars:

        char = color_to_ascii[std_color(bar.get_facecolor())]

        canvas_bar = AsciiCanvas(
                draw_bar(
                bar.get_height(),
                bar.get_width(),
                axes_height,
                axes_width,
                x_range,
                y_range,
                char
            )
        )
        ascii_x_bar = round(linear_transform(bar.xy[0], x_min, x_max, 0, axes_width-1))
        ascii_y_bar = round(linear_transform(bar.xy[1], y_min, y_max, 1, axes_height))

        canvas = canvas.update(canvas_bar, (axes_height - ascii_y_bar - canvas_bar.shape[0]+1, ascii_x_bar))

    return canvas
