import matplotlib
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.contour import QuadContourSet
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Annotation, Text
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.bar import add_bar_chart, draw_bar
from mpl_ascii.color import std_color
from mpl_ascii.line import add_errorbars, add_line_markers, get_lines_with_markers
from mpl_ascii.line import add_line_plots, draw_line
from mpl_ascii.poly import add_violin_plots
from mpl_ascii.scatter import add_scatter_plots
from mpl_ascii.tools import linear_transform

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

    canvas = add_bar_chart(canvas, ax, axes_height, axes_width, x_range, y_range, color_to_ascii)

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

    canvas = add_line_plots(canvas, ax, axes_height, axes_width, x_range, y_range, color_to_ascii)

    canvas = add_errorbars(canvas, ax, axes_height, axes_width, x_range, y_range)

    lines_with_markers = get_lines_with_markers(ax)

    canvas = add_line_markers(canvas, axes_height, axes_width, x_range, y_range, color_to_ascii, lines_with_markers)

    if mpl_ascii.UNRELEASED:
        canvas = add_contours(canvas, ax.collections, axes_height, axes_width, x_range, y_range, color_to_ascii)

    canvas = add_violin_plots(canvas, ax, axes_height, axes_width, x_range, y_range, color_to_ascii)

    canvas = add_scatter_plots(canvas, ax, axes_height, axes_width, x_range, y_range, color_to_ascii)


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