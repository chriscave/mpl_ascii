import math
import numpy as np

from mpl_ascii.tools import linear_transform, scale_factor


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


def draw_line(height, width, x_data, y_data, x_range, y_range, char):

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

    line_canvas_arr = np.full((height, width), fill_value=" ")

    start_points = zip(ascii_x_data[:-1], ascii_y_data[:-1])
    end_points = zip(ascii_x_data[1:], ascii_y_data[1:])
    join_line_points = []
    for start, end in zip(start_points, end_points):
        line_points = bresenham_line(start[0], start[1], end[0], end[1])
        if len(line_points) > 2:
            join_line_points += line_points[1:-1]

    for x, y in zip(ascii_x_data, ascii_y_data):
        row = height - y
        col = x
        line_canvas_arr[row, col] = char

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


