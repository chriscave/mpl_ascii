from matplotlib.collections import PathCollection
from matplotlib.container import BarContainer
from matplotlib.patches import Rectangle


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

line_char = [
    "+",
    "o",
    "a",
    "r",
    "t",
    "d",
    "y",
    "~",
    "!"
]

scatter_char = [
    "x",
    "*",
    "v",
    "z",
    "s",
    "i",
    "n",
]

def map_color_to_ascii(ax):

    def ascii_chars(ls):
        index = 0
        while True:
            yield ls[index]
            index = (index + 1) % len(ls)

    gen = ascii_chars(bar_chars)
    color_to_ascii = {}
    for container in ax.containers:
        if not isinstance(container, BarContainer):
            continue
        for bar in container.patches:
            if not isinstance(bar, Rectangle):
                continue
            color = bar.get_facecolor()
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = next(gen)

    lines = ax.get_lines()
    gen = ascii_chars(line_char)
    for line in lines:
        color = line.get_color()
        if color in color_to_ascii:
            continue
        color_to_ascii[color] = next(gen)


    gen = ascii_chars(scatter_char)
    for collection in ax.collections:
        if not isinstance(collection, PathCollection):
            continue
        for color in collection.get_facecolor():
            color = tuple(color.tolist())
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = next(gen)
    return color_to_ascii
