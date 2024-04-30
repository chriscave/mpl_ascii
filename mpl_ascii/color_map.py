import matplotlib
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

class Char:
    def __init__(self, character: str, color: str) -> None:
        self.character=character
        self.color=color

    def __str__(self) -> str:
        return self.character


    def __rich__(self) -> str:
        return f"[{self.color}]{self.character}[/{self.color}]"

def ax_color_map(ax):

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
            color = std_color(bar.get_facecolor())
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = Char(next(gen), color)

    lines = ax.get_lines()
    gen = ascii_chars(line_chars)
    for line in lines:
        color = std_color(line.get_color())
        if color in color_to_ascii:
            continue
        color_to_ascii[color] = Char(next(gen), color)


    gen = ascii_chars(scatter_chars)
    for collection in ax.collections:
        if not isinstance(collection, PathCollection):
            continue
        for color in collection.get_facecolor():
            color = std_color(tuple(color.tolist()))
            if color in color_to_ascii:
                continue
            color_to_ascii[color] = Char(next(gen), color)

    return color_to_ascii

def std_color(color):
    return matplotlib.colors.to_hex(color)