from typing import Any, Dict, List
from matplotlib.collections import QuadMesh

from mpl_ascii.ax import AxesPlot, get_plots, has_colorbar
from mpl_ascii.bar import get_bars
from mpl_ascii.color import Char, std_color
from mpl_ascii.colorbar import get_colorbar
from mpl_ascii.contour import get_contour_plots
from mpl_ascii.line import get_lines_plots
from mpl_ascii.poly import get_violin_plots
from mpl_ascii.scatter import ScatterPlot, get_scatter_plots

bar_chars = [
    "#",
    "%",
    "&",
    "@",
    "$",
    "=",
    "?",
    "<",
    ">",
    "!",
    "^",
    "~"
]

line_chars = [
    "+",
    "o",
    "a",
    "r",
    "t",
    "d",
    "y",
    "~",
    "[",
    "]",
    "{",
    "}",
]

scatter_chars = [
    "x",
    "v",
    "z",
    "s",
    "i",
    "n",
]



class FigureColorMap:
    def __init__(self, all_axes_plots: List[AxesPlot]) -> None:
        self.all_axes_plots = all_axes_plots

    def associate_color_bar(self, axes_plot: AxesPlot):

        index = self.all_axes_plots.index(axes_plot)
        if index == len(self.all_axes_plots) - 1:
            return None

        colorbar_ax = self.all_axes_plots[index + 1]
        if colorbar_ax.is_colorbar():
            return colorbar_ax.plots[0]

        return None

    def __call__(self, axes_plot: AxesPlot) -> Any:

        cbplot = self.associate_color_bar(axes_plot)

        if not cbplot:
            return ax_color_map(axes_plot.ax)

        color_to_ascii = {}
        color_bar_map = ax_color_map(cbplot.ax)
        tick_data = cbplot.tick_data
        cmap, norm = cbplot.cmap, cbplot.norm
        for plot in axes_plot.plots:
            if type(plot) == ScatterPlot:
                scatter_plot = plot
                for values, colors in zip(scatter_plot.values, scatter_plot.colors):

                    for val, color in zip(values, colors):
                        min_greater = min([tick for tick in tick_data if tick >= val])
                        color = std_color(color)
                        char = color_bar_map[std_color(cmap(norm(min_greater)))]
                        if color in color_to_ascii:
                            continue
                        color_to_ascii[color] = char
                return color_to_ascii

        return ax_color_map(axes_plot.ax)

def ax_color_map(ax):

    def ascii_chars(ls):
        index = 0
        while True:
            yield ls[index]
            index = (index + 1) % len(ls)

    gen = ascii_chars(bar_chars)
    color_to_ascii = {}
    bars = get_bars(ax)
    for bar in bars:
        color = std_color(bar.get_facecolor())
        if color in color_to_ascii:
            continue
        color_to_ascii[color] = Char(next(gen), color)

    gen = ascii_chars(bar_chars)
    for container in ax.collections:
        if not isinstance(container, QuadMesh):
            continue
        tick_data = [tick.get_loc() for tick in ax.yaxis.get_major_ticks()]
        cmap, norm = container.cmap, container.norm
        for td in tick_data:
            color = std_color(cmap(norm(td)))
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = Char(next(gen), color)

    gen = ascii_chars(line_chars)
    lines = get_lines_plots(ax)
    for line in lines:
        color = std_color(line.get_color())
        if color in color_to_ascii:
            continue
        color_to_ascii[color] = Char(next(gen), color)

    pcolls, linecolls = get_violin_plots(ax)
    for collection in pcolls:
        for color in collection.get_facecolor():
            color = std_color(tuple(color.tolist()))
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = Char(next(gen), color)

    for collection in linecolls:
        for color in collection.get_color():
            color = std_color(tuple(color.tolist()))
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = Char(next(gen), color)

    gen = ascii_chars(scatter_chars)
    collection = get_scatter_plots(ax)
    for collection in ax.collections:
        for color in collection.get_facecolor():
            color = std_color(tuple(color.tolist()))
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = Char(next(gen), color)

    gen = ascii_chars(line_chars)
    contour_plots = get_contour_plots(ax)
    if contour_plots:
        for color in contour_plots.colors:
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = Char(next(gen), color)
    return color_to_ascii
