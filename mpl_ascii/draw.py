from itertools import zip_longest
import matplotlib
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection, PathCollection, PolyCollection, QuadMesh
from matplotlib.colors import Colormap, ListedColormap, Normalize
from matplotlib.container import BarContainer, ErrorbarContainer
from matplotlib.contour import QuadContourSet
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Annotation, Text
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.color_map import Char, std_color
from mpl_ascii.tools import linear_transform, scale_factor

from mpl_ascii import color_map

import mpl_ascii

mpl_version = matplotlib.__version__
mpl_version = tuple(map(int, mpl_version.split(".")))


def draw_ax(ax: Axes, axes_height, axes_width, color_to_ascii):
    frame_buffer_left = 1
    frame_buffer_right = 1
    frame_buffer_top = 1
    frame_buffer_bottom = 1


    frame_width = axes_width + frame_buffer_left + frame_buffer_right
    frame_height = axes_height + frame_buffer_top + frame_buffer_bottom

    x_range = ax.get_xlim()
    if x_range[1] < x_range[0]:
        x_range = x_range[1], x_range[0]

    y_range = ax.get_ylim()
    if y_range[1] < y_range[0]:
        y_range = y_range[1], y_range[0]

    canvas = AsciiCanvas(np.full((axes_height, axes_width), fill_value=" "))

    errorbar_caplines, error_barlinescols = get_errorbars(ax.containers)

    canvas = add_bar_chart(canvas, ax.containers, axes_height, axes_width, x_range, y_range, color_to_ascii)

    if mpl_ascii.UNRELEASED:

        for container in ax.collections:
            if isinstance(container, QuadMesh):
                color_bar_width = 10
                axes_width = color_bar_width
                frame_width = axes_width + frame_buffer_left + frame_buffer_right


                bar_chars = color_map.bar_chars
                tick_data = [tick.get_loc() for tick in ax.yaxis.get_major_ticks()]
                for char, i in zip(bar_chars, range(1, len(tick_data))):
                    top_value = tick_data[i]
                    bottom_value = tick_data[i-1]
                    if tick_data[i] > y_range[1]:
                        top_value = y_range[1]
                    top = round(linear_transform(top_value, y_range[0], y_range[1], 1, axes_height))
                    bottom = round(linear_transform(bottom_value, y_range[0], y_range[1], 1, axes_height))
                    cmap, norm = container.cmap, container.norm
                    char = color_to_ascii[std_color(cmap(norm(top_value)))]
                    bar_height = top - bottom
                    if i == 1:
                        bar_height = top

                    c = AsciiCanvas(draw_bar(
                        bar_height,
                        10,
                        axes_height,
                        10,
                        (0,9),
                        (1,axes_height),
                        char
                    ))

                    canvas = canvas.update(c, (axes_height - top, 0))

    canvas = add_line_plots(canvas, ax.get_lines(), axes_height, axes_width, x_range, y_range, color_to_ascii, errorbar_caplines)

    canvas = add_errorbars(canvas, axes_height, axes_width, error_barlinescols, x_range, y_range)

    lines_with_markers = get_lines_with_markers(ax.get_lines(), errorbar_caplines)

    canvas = add_line_markers(canvas, axes_height, axes_width, x_range, y_range, color_to_ascii, lines_with_markers)

    if mpl_ascii.UNRELEASED:
        canvas = add_contours(canvas, ax.collections, axes_height, axes_width, x_range, y_range, color_to_ascii)

    canvas = add_violin_plots(canvas, ax.collections, axes_height, axes_width, x_range, y_range, color_to_ascii, error_barlinescols)

    canvas = add_scatter_plots(canvas, ax.collections, axes_height, axes_width, x_range, y_range, color_to_ascii)


    if mpl_ascii.UNRELEASED:
        canvas = add_text(canvas, ax.texts, axes_height, axes_width, x_range, y_range)

    canvas = add_frame(canvas, frame_height, frame_width, frame_buffer_left, frame_buffer_top)

    canvas = add_xticks_and_labels(canvas, ax, axes_width, x_range)

    canvas = add_yticks_and_labels(canvas, ax, axes_height, y_range)

    canvas = add_ax_title(canvas, ax.get_title())

    canvas = add_legend(canvas, ax.get_legend(), color_to_ascii)

    return canvas


def draw_frame(height, width):
    frame = np.full((height, width), fill_value=" ")
    frame[0,:] = "-"
    frame[-1,:] = "-"
    frame[:,0] = "|"
    frame[:,-1] = "|"

    frame[0,0] = "+"
    frame[0,-1] = "+"
    frame[-1,0] = "+"
    frame[-1,-1] = "+"

    return frame


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


    ascii_x_data = [
        round(linear_transform(x, x_min, x_max, 0, width-1)) for x in plot_x if (x <= x_max and x >= x_min)
    ]
    ascii_y_data = [
        round(linear_transform(y, y_min, y_max, 1, height)) for y in plot_y if (y <= y_max and y >= y_min)
    ]

    line_canvas_arr = np.full((height, width), fill_value=" ", dtype="object")

    for x, y in zip(ascii_x_data, ascii_y_data):
        row = height - y
        col = x
        line_canvas_arr[row, col] = char

    if linestyle == "None":
        return line_canvas_arr

    start_points = zip(ascii_x_data[:-1], ascii_y_data[:-1])
    end_points = zip(ascii_x_data[1:], ascii_y_data[1:])
    join_line_points = []
    for start, end in zip(start_points, end_points):
        line_points = bresenham_line(start[0], start[1], end[0], end[1])
        if len(line_points) > 2:
            join_line_points += line_points[1:-1]


    for x,y in join_line_points:
        row = height - y
        col = x
        line_canvas_arr[row, col] = char

    return line_canvas_arr

def draw_bar(bar_height, bar_width, ax_height, ax_width, x_range, y_range, char):
    x_min, x_max = x_range[0], x_range[1]
    y_min, y_max = y_range[0], y_range[1]

    ascii_width_bar = round(bar_width * scale_factor(x_min, x_max, 0, ax_width-1))
    ascii_height_bar = round(bar_height * scale_factor(y_min, y_max, 1, ax_height))

    return np.full((ascii_height_bar, ascii_width_bar), fill_value=char)

def draw_x_ticks(width, tick_data, tick_label_data, x_range):
    x_min, x_max = x_range[0], x_range[1]

    xticks = np.full((2, width), " ")
    for x, label in zip(tick_data, tick_label_data):
        x = round(linear_transform(x, x_min, x_max, 0, width-1))
        if x < 0 or x >= width:
            continue
        xticks[0:1,x] = "|"
        for i, char in enumerate(list(label)):
            xticks[-1, x - len(label) + i+1] = char

    return xticks

def draw_y_ticks(height, tick_data, tick_label_data, y_range):
    y_min, y_max = y_range[0], y_range[1]

    yticks_width = max([len(label) for label in tick_label_data]) + 2
    yticks = np.full((height, yticks_width), " ")

    for y, label in zip(tick_data, tick_label_data):
        y = round(linear_transform(y, y_min, y_max, 1, height))
        if y <= 0 or y > height:
            continue
        row = height - y
        yticks[row,-2:] = "-"
        for i, char in enumerate(list(label)):
            yticks[row, -len(label) - 2 + i] = char

    return yticks


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

def get_errorbars(containers):
    errorbar_caplines = []
    error_barlinescols = []
    for container in containers:
        if not isinstance(container, ErrorbarContainer):
            continue
        _, caplines, barlinescols = tuple(container)
        errorbar_caplines += [*caplines]
        error_barlinescols += [*barlinescols]

    return errorbar_caplines, error_barlinescols

def add_bar_chart(canvas, containers, axes_height, axes_width, x_range, y_range, color_to_ascii):
    x_min, x_max = x_range
    y_min, y_max = y_range

    for container in containers:
        # Draw Bar chart
        if not isinstance(container, BarContainer):
            continue
        for bar in container.patches:
            if not isinstance(bar, Rectangle):
                continue

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

def add_line_plots(canvas, lines, axes_height, axes_width, x_range, y_range, color_to_ascii, errorbar_caplines):
    for line in lines:
        if line in errorbar_caplines:
            continue

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

def get_lines_with_markers(lines, errorbar_caplines):
    lines_with_markers = []
    # Draw lines
    for line in lines:
        if line in errorbar_caplines:
            continue
        if line.get_marker() != "None" and line.get_marker() != "":
            lines_with_markers.append(line)

    return lines_with_markers

def add_errorbars(canvas, axes_height, axes_width, error_barlinescols, x_range, y_range):
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

def add_line_markers(canvas, axes_height, axes_width, x_range, y_range, color_to_ascii, lines_with_markers):
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

def add_violin_plots(canvas, collections, axes_height, axes_width, x_range, y_range, color_to_ascii, error_barlinescols):
    for collection in collections:
        # Contour plot
        if isinstance(collection, PolyCollection):
            char = color_to_ascii[std_color(collection.get_facecolor())]
            for path in collection.get_paths():
                xy_data = path.vertices
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
                    )
                )
                canvas = canvas.update(line, (0,0))

        if isinstance(collection, LineCollection):
            if collection in error_barlinescols:
                continue

            for xy in collection.get_segments():
                x_data = [p[0] for p in xy]
                y_data = [p[1] for p in xy]
                char = color_to_ascii[std_color(collection.get_color())]
                line = AsciiCanvas(
                    draw_line(
                    width=axes_width,
                    height=axes_height,
                    x_data=x_data,
                    y_data=y_data,
                    x_range=x_range,
                    y_range=y_range,
                    char = char,
                    )
                )
                canvas = canvas.update(line, (0,0))
    return canvas

def add_scatter_plots(canvas, collections, axes_height, axes_width, x_range, y_range, color_to_ascii):
    x_min, x_max = x_range
    y_min, y_max = y_range

    for collection in collections:
        # Add scatter plot
        if isinstance(collection, PathCollection):
            offsets = collection.get_offsets()
            if len(collection.get_facecolor()) > 0:
                default_color = collection.get_facecolor()[0]
                colors = collection.get_facecolor()

            if len(collection.get_edgecolor()) > 0:
                default_color = collection.get_edgecolor()[0]
                colors = collection.get_edgecolor()


            for point,color in zip_longest(offsets, colors, fillvalue=default_color):
                color = tuple(color)

                x_new = round(linear_transform(point[0], x_min, x_max, 0, axes_width-1))
                y_new = round(linear_transform(point[1], y_min, y_max, 1, axes_height))

                char = color_to_ascii.get(std_color(color), Char("+", "white"))
                canvas = canvas.update(AsciiCanvas(np.array([[char]])), (axes_height-y_new, x_new))

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

def add_frame(canvas, frame_height, frame_width, frame_buffer_left, frame_buffer_top):
    canvas = canvas.update(AsciiCanvas(draw_frame(frame_height, frame_width)), (-frame_buffer_left,-frame_buffer_top))
    return canvas

def add_xticks_and_labels(canvas, ax, axes_width, x_range):
    tick_data = [tick.get_position()[0] for tick in ax.xaxis.get_ticklabels()]
    label_data = [tick.get_text().replace("\n", "") for tick in ax.xaxis.get_ticklabels()]
    xticks = AsciiCanvas(draw_x_ticks(axes_width, tick_data, label_data, x_range))

    xlabel = AsciiCanvas(np.array([list(ax.get_xlabel())]))

    xticks_and_label = xticks.update(xlabel, location=(xticks.shape[0],int(xticks.shape[1] / 2)))

    canvas = canvas.update(xticks_and_label, location=(canvas.shape[0]-1, 1))
    return canvas

def add_yticks_and_labels(canvas, ax, axes_height, y_range):

    # Add yticks and labels
    tick_data = [tick.get_loc() for tick in ax.yaxis.get_major_ticks()]
    label_data = [tick.label1.get_text().replace("\n", "") for tick in ax.yaxis.get_major_ticks()]
    yticks = AsciiCanvas(draw_y_ticks(axes_height, tick_data, label_data, y_range))

    ylabel = AsciiCanvas(np.array([list(ax.get_ylabel())]).T)
    yticks_and_label = yticks.update(ylabel, location=(int(yticks.shape[0] / 2), -(ylabel.shape[1] + 1)))

    canvas = canvas.update(yticks_and_label, location=(1, -yticks_and_label.shape[1]+1))
    return canvas

def add_ax_title(canvas, title):
    ax_title = AsciiCanvas(np.array([list(title)]))
    canvas = canvas.update(ax_title, location=(-(ax_title.shape[0] + 1), int(canvas.shape[1] / 2)))

    return canvas

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

        canvas = canvas.update(canvas_legend, (canvas.shape[0] + 1, round(canvas.shape[1] / 2) ))

    return canvas