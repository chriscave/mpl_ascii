import matplotlib
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.text import Annotation, Text
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.tools import linear_transform, get_xrange, get_yrange

mpl_version = matplotlib.__version__
mpl_version = tuple(map(int, mpl_version.split(".")))

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

def draw_y_ticks(height, tick_data, tick_label_data, y_range, tick_params):
    y_min, y_max = y_range[0], y_range[1]

    yticks_width = max([len(label) for label in tick_label_data]) + 2
    yticks = np.full((height, yticks_width), " ")

    for y, label in zip(tick_data, tick_label_data):
        y = round(linear_transform(y, y_min, y_max, 1, height))
        if y <= 0 or y > height:
            continue
        row = height - y
        if tick_params.get("labelright"):
            yticks[row,:2] = "-"
            for i, char in enumerate(list(label)):
                yticks[row, 2 + i] = char
        else:
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

def add_yticks_and_labels(canvas, ax: Axes, axes_height):
    y_range = get_yrange(ax)
    tick_data = [tick.get_loc() for tick in ax.yaxis.get_major_ticks()]
    label_data = [tick.label1.get_text().replace("\n", "") for tick in ax.yaxis.get_major_ticks()]
    if mpl_version >= (3,7,0):
        tick_params = ax.yaxis.get_tick_params()
    else:
        tick_params = get_tick_params(ax.yaxis)
    yticks = AsciiCanvas(draw_y_ticks(axes_height, tick_data, label_data, y_range, tick_params))

    ylabel = AsciiCanvas(np.array([list(ax.get_ylabel())]).T)
    if tick_params.get("labelright"):
        yticks_and_label = yticks.update(ylabel, location=(int(yticks.shape[0] / 2), yticks.shape[1]))
        canvas = canvas.update(yticks_and_label, location=(1, canvas.shape[1] - 1))

    else:
        yticks_and_label = yticks.update(ylabel, location=(int(yticks.shape[0] / 2), -(ylabel.shape[1] + 1)))
        canvas = canvas.update(yticks_and_label, location=(1, -yticks_and_label.shape[1]+1))
    return canvas

def add_ax_title(canvas, title):
    ax_title = AsciiCanvas(np.array([list(title)]))
    canvas = canvas.update(ax_title, location=(-(ax_title.shape[0] + 1), int(canvas.shape[1] / 2)))

    return canvas

def add_text(canvas, ax: Axes):
    texts = ax.texts
    x_min, x_max = get_xrange(ax)
    y_min, y_max = get_yrange(ax)
    axes_height, axes_width = canvas.shape

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


import matplotlib.artist as martist
import matplotlib.lines as mlines

_line_inspector = martist.ArtistInspector(mlines.Line2D)
_line_param_names = _line_inspector.get_setters()
_line_param_aliases = [list(d)[0] for d in _line_inspector.aliasd.values()]
_gridline_param_names = ['grid_' + name
                         for name in _line_param_names + _line_param_aliases]


def get_tick_params(axis: Axis, which='major'):
    from matplotlib import _api
    _api.check_in_list(['major', 'minor'], which=which)
    if which == 'major':
        return _translate_tick_params(
            axis._major_tick_kw, reverse=True
        )
    return _translate_tick_params(axis._minor_tick_kw, reverse=True)

def _translate_tick_params(kw, reverse=False):
    kw_ = {**kw}

    # The following lists may be moved to a more accessible location.
    allowed_keys = [
        'size', 'width', 'color', 'tickdir', 'pad',
        'labelsize', 'labelcolor', 'labelfontfamily', 'zorder', 'gridOn',
        'tick1On', 'tick2On', 'label1On', 'label2On',
        'length', 'direction', 'left', 'bottom', 'right', 'top',
        'labelleft', 'labelbottom', 'labelright', 'labeltop',
        'labelrotation',
        *_gridline_param_names]

    keymap = {
        # tick_params key -> axis key
        'length': 'size',
        'direction': 'tickdir',
        'rotation': 'labelrotation',
        'left': 'tick1On',
        'bottom': 'tick1On',
        'right': 'tick2On',
        'top': 'tick2On',
        'labelleft': 'label1On',
        'labelbottom': 'label1On',
        'labelright': 'label2On',
        'labeltop': 'label2On',
    }
    if reverse:
        kwtrans = {
            oldkey: kw_.pop(newkey)
            for oldkey, newkey in keymap.items() if newkey in kw_
        }
    else:
        kwtrans = {
            newkey: kw_.pop(oldkey)
            for oldkey, newkey in keymap.items() if oldkey in kw_
        }
    if 'colors' in kw_:
        c = kw_.pop('colors')
        kwtrans['color'] = c
        kwtrans['labelcolor'] = c
    # Maybe move the checking up to the caller of this method.
    for key in kw_:
        if key not in allowed_keys:
            raise ValueError(
                "keyword %s is not recognized; valid keywords are %s"
                % (key, allowed_keys))
    kwtrans.update(kw_)
    return kwtrans