from typing import Dict
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.figure import Figure

from mpl_ascii.bar import get_bars
from mpl_ascii.color import Char, std_color
from mpl_ascii.line import get_lines_plots
from mpl_ascii.poly import get_violin_plots
from mpl_ascii.scatter import get_scatter_plots


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
    def __init__(self, figure: Figure) -> None:
        self.figure = figure

    def associate_color_bar(self, ax):
        ax_idx = self.figure.axes.index(ax)
        if ax_idx == len(self.figure.axes) - 1:
            return None

        color_bar = self.figure.axes[ax_idx+1]
        for container in color_bar.collections:
            if isinstance(container, QuadMesh):
                return color_bar

        return None

    def __call__(self, ax: Axes) -> Dict:
        colorbar = self.associate_color_bar(ax)
        if colorbar is None:
            return ax_color_map(ax)

        color_bar_map = ax_color_map(colorbar)

        for collection in colorbar.collections:
            if isinstance(collection, QuadMesh):
                cmap, norm = collection.cmap, collection.norm



        tick_data = [tick.get_loc() for tick in colorbar.yaxis.get_major_ticks()]

        color_to_ascii = {}
        for collection in ax.collections:
            if isinstance(collection, PathCollection):
                for val, color in zip(collection.get_array(), collection.get_facecolor()):
                    min_greater = min([tick for tick in tick_data if tick >= val])
                    color = std_color(color)
                    char = color_bar_map[std_color(cmap(norm(min_greater)))]
                    if color in color_to_ascii:
                        continue
                    color_to_ascii[color] = char

        return color_to_ascii



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

    return color_to_ascii
