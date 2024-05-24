from matplotlib.axes import Axes
from matplotlib.collections import PathCollection, QuadMesh
import numpy as np

import mpl_ascii
from mpl_ascii.ascii_canvas import AsciiCanvas
from mpl_ascii.bar import BarPlots, get_bars
from mpl_ascii.color import std_color
from mpl_ascii.color_map import ax_color_map
from mpl_ascii.colorbar import ColorbarPlot, get_colorbar
from mpl_ascii.format import add_ax_title, add_ticks_and_frame
from mpl_ascii.legend import add_legend
from mpl_ascii.line import Errorbars, LineMarkers, LinePlots, get_errorbars, get_lines_plots, get_lines_with_markers
from mpl_ascii.poly import ViolinPlots, get_violin_plots
from mpl_ascii.scatter import ScatterPlot, get_scatter_plots


class AxesPlot:
    def __init__(self, ax, axes_height, axes_width, colorbar=None) -> None:
        self.ax = ax
        self.plots = get_plots(ax)
        self._axes_height = axes_height
        self._axes_width = axes_width
        # self.color_to_ascii = color_to_ascii
        self._colorbar = colorbar


    def color_to_ascii(self):
        # if not self.colorbar:
        #     color_to_ascii = {}
        #     colors = []
        #     for plot in self.plots:
        #         colors.append(plot.colors)

        if not self.colorbar:
            return ax_color_map(self.ax)

        if self.colorbar:
            colorbar = self.colorbar.ax
            color_bar_map = ax_color_map(colorbar)

            for collection in colorbar.collections:
                if isinstance(collection, QuadMesh):
                    cmap, norm = collection.cmap, collection.norm



            tick_data = [tick.get_loc() for tick in colorbar.yaxis.get_major_ticks()]

            color_to_ascii = {}
            for collection in self.ax.collections:
                if isinstance(collection, PathCollection):
                    for val, color in zip(collection.get_array(), collection.get_facecolor()):
                        min_greater = min([tick for tick in tick_data if tick >= val])
                        color = std_color(color)
                        char = color_bar_map[std_color(cmap(norm(min_greater)))]
                        if color in color_to_ascii:
                            continue
                        color_to_ascii[color] = char

        return color_to_ascii





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

    @property
    def colorbar(self):
        return self._colorbar

    @colorbar.setter
    def colorbar(self, colorbar):
        self._colorbar = colorbar

    @property
    def canvas(self):
        return draw_ax(self.ax, self.plots, self.axes_height, self.axes_width, self.color_to_ascii( ))


def draw_ax(ax: Axes, all_plots, axes_height, axes_width, color_to_ascii):

    canvas = init_canvas(all_plots, axes_height, axes_width)

    for plot in all_plots:
        canvas = plot.update(canvas, color_to_ascii)

    canvas = add_ticks_and_frame(canvas, ax)

    canvas = add_ax_title(canvas, ax.get_title())

    canvas = add_legend(canvas, ax.get_legend(), color_to_ascii)

    return canvas

def init_canvas(all_plots, axes_height, axes_width):
    if mpl_ascii.UNRELEASED:
        if type(all_plots[0]) == ColorbarPlot:
            axes_width = 10
    canvas = AsciiCanvas(np.full((axes_height, axes_width), fill_value=" "))
    return canvas

def get_plots(ax):
    all_plots = []
    if has_bar_plots(ax):
        all_plots.append(BarPlots(ax))
    if mpl_ascii.UNRELEASED:
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