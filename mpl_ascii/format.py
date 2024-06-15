import matplotlib
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.text import Annotation, Text
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.tools import linear_transform, get_xrange, get_yrange


MAX_TRUNC_LEN = 10

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

    tick_locations=[]
    visible_labels = []
    for x, label in zip(tick_data, tick_label_data):
        x = round(linear_transform(x, x_min, x_max, 0, width-1))
        if x < 0 or x >= width:
            continue
        tick_locations.append(x)
        visible_labels.append(label)


    tick_locs_and_frame = tick_locations.copy()
    tick_locs_and_frame.insert(0, -1) # include the frame, 0 index is not occupied

    label_idxs = get_xticklabel_loc_idxs(tick_locations, visible_labels, width)
    transpose_labels = False
    for label in label_idxs:
        start, end = label_idxs[label]
        if (end - start) < len(label):
            transpose_labels = True
            break

    if transpose_labels:
        max_label_len = max([len(l) for l in label_idxs])
        xticks = np.full((max_label_len + 1, width), " ")
        for loc, label in zip(tick_locations, label_idxs):
            xticks[0:1,loc] = "|"
            for i, char in enumerate(list(label)):
                xticks[1+i, loc] = char

    else:
        xticks = np.full((2, width), " ")
        for tick_loc, label in zip(tick_locations, label_idxs):
            xticks[0:1,tick_loc] = "|"
            start_idx, _ = label_idxs[label]
            for i, char in enumerate(list(label)):
                xticks[-1, start_idx + i] = char

    return xticks

def get_xticklabel_loc_idxs(tick_loc, labels, xaxis_width):
    trunc_labels = get_trunc_labels(labels, MAX_TRUNC_LEN)
    label_loc = dict()
    prev_end_idx = -1
    for i, (tl, lab, trlab) in enumerate(zip(tick_loc, labels, trunc_labels)):
        label = lab
        next_tick_loc = xaxis_width
        if i < len(tick_loc) - 1:
            next_tick_loc = tick_loc[i+1]

        ll = len(label)
        start_idx = tl - ll + 1
        if start_idx <= prev_end_idx:
            start_idx = tl

        end_idx = start_idx + ll
        if end_idx > next_tick_loc:
            label = trlab
            ll = len(label)
            start_idx = tl - ll + 1
            if start_idx <= prev_end_idx:
                start_idx = tl

            end_idx = start_idx + ll
            if end_idx > next_tick_loc:
                end_idx = start_idx

        prev_end_idx = end_idx
        label_loc[label] = (start_idx, end_idx)

    return label_loc

def get_trunc_labels(labels, trunc_size):
    ellipse = '\u2026'
    lb = 6
    regions = isolate_interesting_regions(labels, trunc_size, lb)
    trunc_labels = []
    for idx, label in enumerate(labels):
        start = regions[idx]
        end = start+trunc_size
        trunc_label = label[start:end]
        if start > 0:
            trunc_label = list(trunc_label)
            trunc_label[0] = ellipse
            trunc_label = "".join(trunc_label)
        if end < len(label):
            trunc_label = list(trunc_label)
            trunc_label[-1] = ellipse
            trunc_label = "".join(trunc_label)

        trunc_labels.append(trunc_label)

    return trunc_labels



def draw_y_ticks(height, tick_data, tick_label_data, y_range, tick_params):
    y_min, y_max = y_range[0], y_range[1]
    labels = get_trunc_labels(tick_label_data, MAX_TRUNC_LEN)

    yticks_width = max([len(label) for label in labels]) + 2
    yticks = np.full((height, yticks_width), " ")


    for y, label in zip(tick_data, labels):
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

    xlabel = ax.get_xlabel()
    start_idx = int((xticks.shape[1] / 2) - (len(xlabel) / 2))
    if start_idx < 0:
        xlabel = get_trunc_labels([xlabel], trunc_size=xticks.shape[0] - 1)

    xlabel = AsciiCanvas(np.array([list(xlabel)]))

    xticks_and_label = xticks.update(xlabel, location=(xticks.shape[0],start_idx))

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

    ylabel = ax.get_ylabel()
    start_idx = int((yticks.shape[0] / 2) - (len(ylabel) / 2))
    if start_idx < 0:
        ylabel = get_trunc_labels([ylabel], trunc_size=yticks.shape[0] - 1)

    ylabel = AsciiCanvas(np.array([list(ylabel)]).T)
    if tick_params.get("labelright"):
        yticks_and_label = yticks.update(ylabel, location=(start_idx, yticks.shape[1]))
        canvas = canvas.update(yticks_and_label, location=(1, canvas.shape[1] - 1))

    else:
        yticks_and_label = yticks.update(ylabel, location=(start_idx, -(ylabel.shape[1] + 1)))
        canvas = canvas.update(yticks_and_label, location=(1, -yticks_and_label.shape[1]+1))
    return canvas

def add_ax_title(canvas, title):

    start_idx = int((canvas.shape[1] / 2) - (len(title) / 2))
    if start_idx < 0:
        title = get_trunc_labels([title], trunc_size=canvas.shape[1] - 1)

    ax_title = AsciiCanvas(np.array([list(title)]))
    canvas = canvas.update(ax_title, location=(-(ax_title.shape[0] + 1), start_idx))

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

def isolate_interesting_regions(strs, trunc_size=10, lb=3):
    regions = []
    for i, me in enumerate(strs):
        i_regions = []
        others = strs[:i] + strs[i + 1 :]
        if i < len(strs):
            for other in others:
                if _compare(me, other, trunc_size) > 0:
                    reg_start = _spool(me, other, lb=lb)
                    i_regions.append(reg_start)

        any_safe = False
        for reg in i_regions:
            if _is_region_cross_safe(me, others, reg, trunc_size):
                regions.append(reg)
                any_safe |= True
                break
        if not any_safe:
            regions.append(0)

    return regions


def _compare(me, other, trunc_size):
    if me == other:
        return -1
    if me[:trunc_size] == other[:trunc_size]:
        return 1
    else:
        return 0


def _spool(me, other, lb):
    start = 0
    for i, (c1, c2) in enumerate(zip(me, other)):
        if c1 == c2:
            continue
        start = i - lb
        break
    return max(start, 0)


def _is_region_cross_safe(me, others, region, trunc_size):
    safe = True
    for other in others:
        safe &= me[region : region + trunc_size] != other[region : region + trunc_size]

    return safe
