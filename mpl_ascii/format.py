import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.tools import linear_transform, get_xrange, get_yrange


def add_ticks_and_frame(canvas, ax):
    axes_height, axes_width = canvas.shape
    canvas = add_frame(canvas)
    canvas = add_xticks_and_labels(canvas, ax, axes_width)
    canvas = add_yticks_and_labels(canvas, ax, axes_height)
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

def add_frame(canvas):
    axes_height, axes_width = canvas.shape
    frame_buffer_left = 1
    frame_buffer_right = 1
    frame_buffer_top = 1
    frame_buffer_bottom = 1
    frame_width = axes_width + frame_buffer_left + frame_buffer_right
    frame_height = axes_height + frame_buffer_top + frame_buffer_bottom

    canvas = canvas.update(AsciiCanvas(draw_frame(frame_height, frame_width)), (-frame_buffer_left,-frame_buffer_top))
    return canvas

def add_xticks_and_labels(canvas, ax, axes_width):
    x_range = get_xrange(ax)
    tick_data = [tick.get_position()[0] for tick in ax.xaxis.get_ticklabels()]
    label_data = [tick.get_text().replace("\n", "") for tick in ax.xaxis.get_ticklabels()]
    xticks = AsciiCanvas(draw_x_ticks(axes_width, tick_data, label_data, x_range))

    xlabel = AsciiCanvas(np.array([list(ax.get_xlabel())]))

    xticks_and_label = xticks.update(xlabel, location=(xticks.shape[0],int(xticks.shape[1] / 2)))

    canvas = canvas.update(xticks_and_label, location=(canvas.shape[0]-1, 1))
    return canvas

def add_yticks_and_labels(canvas, ax, axes_height):
    y_range = get_yrange(ax)
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
