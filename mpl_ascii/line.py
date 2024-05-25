from matplotlib.axes import Axes
from matplotlib.container import ErrorbarContainer
import numpy as np
from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color import std_color
from mpl_ascii.color import Char
from mpl_ascii.tools import linear_transform, get_xrange, get_yrange


class LinePlots:
    def __init__(self, ax) -> None:
        self.ax = ax
    def update(self, canvas, color_to_ascii):
        return add_line_plots(canvas, self.ax, color_to_ascii)

class Errorbars:
    def __init__(self, ax) -> None:
        self.ax = ax
    def update(self, canvas, color_to_ascii):
        return add_errorbars(canvas, self.ax)

class LineMarkers:
    def __init__(self, ax) -> None:
        self.ax = ax

    def update(self, canvas, color_to_ascii):
        return add_line_markers(canvas, self.ax, color_to_ascii)


def get_lines_plots(ax: Axes):
    errorbar_caplines, _ = get_errorbars(ax)
    lines = []
    for line in ax.get_lines():
        if line in errorbar_caplines:
            continue
        lines.append(line)
    return lines



def add_line_plots(canvas, ax, color_to_ascii):
    x_range, y_range = get_xrange(ax), get_yrange(ax)
    axes_height, axes_width = canvas.shape
    for line in get_lines_plots(ax):

        char = color_to_ascii[std_color(line.get_color())]
        xy_data = line.get_xydata()
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
                linestyle=line.get_linestyle()
            )
        )

        canvas = canvas.update(line, (0,0))
    return canvas

def draw_line(height, width, x_data, y_data, x_range, y_range, char, linestyle="-"):

    x_min, x_max = x_range[0], x_range[1]
    y_min, y_max = y_range[0], y_range[1]

    plot_x = []
    plot_y = []
    for x,y in zip(x_data, y_data):
        if x < x_min or x > x_max:
            continue
        if y < y_min or y > y_max:
            continue
        plot_x.append(x)
        plot_y.append(y)


    ascii_x_data = []
    for x in plot_x:
        if np.isnan(x):
            ascii_x_data.append(None)
            continue
        ascii_x_data.append(round(linear_transform(x, x_min, x_max, 0, width-1)))

    ascii_y_data = []
    for y in plot_y:
        if np.isnan(y):
            ascii_y_data.append(None)
            continue
        ascii_y_data.append(round(linear_transform(y, y_min, y_max, 1, height)))


    line_canvas_arr = np.full((height, width), fill_value=" ", dtype="object")

    for x, y in zip(ascii_x_data, ascii_y_data):
        if x is None or y is None:
            continue
        row = height - y
        col = x
        line_canvas_arr[row, col] = char

    if linestyle == "None":
        return line_canvas_arr

    start_points = zip(ascii_x_data[:-1], ascii_y_data[:-1])
    end_points = zip(ascii_x_data[1:], ascii_y_data[1:])
    join_line_points = []
    for start, end in zip(start_points, end_points):
        if start[0] is None or start[1] is None:
            continue
        if end[0] is None or end[1] is None:
            continue
        line_points = bresenham_line(start[0], start[1], end[0], end[1])
        if len(line_points) > 2:
            join_line_points += line_points[1:-1]


    for x,y in join_line_points:
        row = height - y
        col = x
        line_canvas_arr[row, col] = char

    return line_canvas_arr

def bresenham_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line if it's steep
    if is_steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    # Swap start and end points if necessary
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # Recalculate differences
    dx = x1 - x0
    dy = y1 - y0

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y0 < y1 else -1

    # Iterate over bounding box generating points between start and end
    y = y0
    points = []
    for x in range(x0, x1 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    return points


def get_errorbars(ax):
    errorbar_caplines = []
    error_barlinescols = []
    for container in ax.containers:
        if not isinstance(container, ErrorbarContainer):
            continue
        _, caplines, barlinescols = tuple(container)
        errorbar_caplines += [*caplines]
        error_barlinescols += [*barlinescols]

    return errorbar_caplines, error_barlinescols

def add_errorbars(canvas, ax):
    x_range, y_range = get_xrange(ax), get_yrange(ax)
    axes_height, axes_width = canvas.shape
    _, error_barlinescols = get_errorbars(ax)
    for collection in error_barlinescols:
        for xy in collection.get_segments():
            x_data = [p[0] for p in xy]
            y_data = [p[1] for p in xy]
            char = Char("-", "white")

            if len(set(x_data)) == 1:
                char = Char("|", "white")

            errorbar = AsciiCanvas(draw_line(
                width=axes_width,
                height=axes_height,
                x_data=x_data,
                y_data=y_data,
                x_range=x_range,
                y_range=y_range,
                char = char
            ))

            canvas = canvas.update(errorbar, (0,0))
    return canvas

def get_ascii_marker(marker):
    if marker == "s":
        marker = chr(9632)
    if marker == "o":
        marker = "O"
    if marker == "v" or marker == "1":
        marker = chr(9660)
    if marker == "^" or marker == "2":
        marker = chr(9650)
    if marker == "<" or marker == "3":
        marker = chr(9664)
    if marker == ">" or marker == "4":
        marker = chr(9654)

    return marker

def get_lines_with_markers(ax):

    lines = get_lines_plots(ax)
    lines_with_markers = []
    # Draw lines
    for line in lines:
        if line.get_marker() != "None" and line.get_marker() != "":
            lines_with_markers.append(line)

    return lines_with_markers

def add_line_markers(canvas, ax, color_to_ascii):
    x_range, y_range = get_xrange(ax), get_yrange(ax)
    axes_height, axes_width = canvas.shape
    lines_with_markers = get_lines_with_markers(ax)
    for line in lines_with_markers:
        marker = get_ascii_marker(line.get_marker())

        color = color_to_ascii[std_color(line.get_color())].color
        char = Char(marker.upper(), color)
        xy_data = line.get_xydata()
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
                linestyle="None"
            )
        )
        canvas = canvas.update(line, (0,0))
    return canvas
