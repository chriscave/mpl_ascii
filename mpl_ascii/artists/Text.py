from matplotlib.text import Text

from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import TextElement


def parse(text: Text) -> TextElement:

    s = text.get_text()

    x, y = text.get_position()

    anchor = Point(x,y)

    halign = text.get_horizontalalignment()
    valign = text.get_verticalalignment()


    return TextElement(s, anchor, to_mapping(text.get_transform()), halign, valign)