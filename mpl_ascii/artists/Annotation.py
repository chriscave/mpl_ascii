from typing import Callable
from matplotlib.text import Annotation
from matplotlib.transforms import BboxTransformTo

from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import TextElement


def parse(obj: Annotation) -> TextElement:

    text = obj.get_text()
    x: float
    y: float
    x,y = obj.xy # type: ignore
    anchor = Point(x,y) # type: ignore

    if isinstance(obj.xycoords, Callable):
        return TextElement(
            text,
            anchor,
            to_mapping(BboxTransformTo(obj.xycoords(obj))),
            "center",
            "center"
        )

    if isinstance(obj.xycoords, str):
        if obj.xycoords == "data":
            return TextElement(
                text,
                anchor,
                to_mapping(obj.axes.transData),
                "center",
                "center"
            )