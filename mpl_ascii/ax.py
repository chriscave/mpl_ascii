from matplotlib.axes import Axes
import numpy as np

from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.bar import BarPlots, get_bars
from mpl_ascii.colorbar import ColorbarPlot, get_colorbar
from mpl_ascii.contour import get_contour_plots
from mpl_ascii.format import add_ax_title, add_text, add_ticks_and_frame
from mpl_ascii.legend import add_legend
from mpl_ascii.line import Errorbars, LineMarkers, LinePlots, get_errorbars, get_lines_plots, get_lines_with_markers
from mpl_ascii.poly import ViolinPlots, get_violin_plots
from mpl_ascii.scatter import ScatterPlot, get_scatter_plots


class AxesPlot:
    def __init__(self, ax, axes_height, axes_width, color_map=None, colorbar=None) -> None:
        self.ax = ax
        self.plots = get_plots(ax)
        self._axes_height = axes_height
        self._axes_width = axes_width
        self._colorbar = colorbar
        self._color_map = color_map
        self._canvas = AsciiCanvas()

    def is_colorbar(self):
        if len(self.plots) > 0 and type(self.plots[0]) == ColorbarPlot:
            return True
        return False

    @property
    def axes_height(self):
        return self._axes_height

    @property
    def axes_width(self):
        if self.is_colorbar():
            return 10
        return self._axes_width

    def draw_canvas(self, color_map):
        self._color_map = color_map
        self._canvas = draw_ax(self.ax, self.plots, self.axes_height, self.axes_width, color_map)
        self.create_color_canvas()

    @property
    def color_map(self):
        return self._color_map

    @property
    def canvas(self):
        return self._canvas

    @property
    def color_canvas(self):
        return self._color_canvas

    def create_color_canvas(self):
        color_canvas = AsciiCanvas(self.canvas.array.copy())
        arr = color_canvas.array
        for color in self.color_map:
            arr[arr==self.color_map[color]]=f"[{color}]{self.color_map[color]}[/{color}]"
            color_canvas.array = arr

        self._color_canvas = color_canvas


def draw_ax(ax: Axes, all_plots, axes_height, axes_width, color_to_ascii):

    canvas = init_canvas(all_plots, axes_height, axes_width)

    for plot in all_plots:
        canvas = plot.update(canvas, color_to_ascii)

    canvas = add_text(canvas, ax)

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

    contour_plots = get_contour_plots(ax)
    if contour_plots:
        all_plots.append(contour_plots)

    if len(all_plots) == 0:
        raise Exception("Sorry, this type of plot is not yet a available for mpl_ascii.\n\
Please submit feature requests to https://github.com/chriscave/mpl_ascii")

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