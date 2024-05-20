import matplotlib
from matplotlib.axes import Axes
from matplotlib.contour import QuadContourSet
from matplotlib.text import Annotation, Text
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.bar import BarPlots, get_bars
from mpl_ascii.colorbar import ColorbarPlot,get_colorbar
from mpl_ascii.format import add_ax_title, add_ticks_and_frame
from mpl_ascii.legend import add_legend
from mpl_ascii.line import Errorbars, LineMarkers, LinePlots, get_errorbars, get_lines_plots, get_lines_with_markers
from mpl_ascii.line import draw_line
from mpl_ascii.poly import ViolinPlots, get_violin_plots
from mpl_ascii.scatter import ScatterPlot, get_scatter_plots
from mpl_ascii.tools import linear_transform


mpl_version = matplotlib.__version__
mpl_version = tuple(map(int, mpl_version.split(".")))


def draw_ax(ax: Axes, all_plots, axes_height, axes_width, color_to_ascii):

    canvas = init_canvas(all_plots, axes_height, axes_width)

    for plot in all_plots:
        canvas = plot.update(canvas, color_to_ascii)

    canvas = add_ticks_and_frame(canvas, ax)

    canvas = add_ax_title(canvas, ax.get_title())

    canvas = add_legend(canvas, ax.get_legend(), color_to_ascii)

    return canvas

def init_canvas(all_plots, axes_height, axes_width):
    if type(all_plots[0]) == ColorbarPlot:
        axes_width = 10
    canvas = AsciiCanvas(np.full((axes_height, axes_width), fill_value=" "))
    return canvas



def get_plots(ax):
    all_plots = []
    if has_bar_plots(ax):
        all_plots.append(BarPlots(ax))
    if has_colorbar(ax):
        all_plots.append(ColorbarPlot(ax))
    if has_line_plots(ax):
        all_plots.append(LinePlots(ax))
    if has_errorbars(ax):
        all_plots.append(Errorbars(ax))
    if has_line_markers(ax):
        all_plots.append(LineMarkers(ax))
    if has_violin_plots(ax):
        all_plots.append(ViolinPlots(ax))
    if has_scatter_plots(ax):
        all_plots.append(ScatterPlot(ax))

    return all_plots

def has_colorbar(ax):
    if get_colorbar(ax):
        return True
    return False

def has_bar_plots(ax):
    if len(get_bars(ax)) > 0:
        return True
    return False

def has_line_plots(ax):
    if len(get_lines_plots(ax)) > 0:
        return True
    return False

def has_errorbars(ax):
    errorbar_caplines, error_barlinescols = get_errorbars(ax)
    if len(errorbar_caplines) > 0 or len(error_barlinescols) > 0:
        return True
    return False

def has_scatter_plots(ax):
    if len(get_scatter_plots(ax)) > 0:
        return True
    return False

def has_line_markers(ax):
    if len(get_lines_with_markers(ax)) > 0:
        return True
    return False

def has_violin_plots(ax):
    pcoll, linecolls = get_violin_plots(ax)
    if len(pcoll) > 0 and len(linecolls) > 0:
        return True
    return False


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
