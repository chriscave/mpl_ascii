from __future__ import annotations
from typing import Union
from matplotlib.axis import YAxis
from matplotlib.lines import Line2D

from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import PointMark, Shape, TextElement

def parse(obj: YAxis) -> list[Union[Shape, TextElement]]:


    y_bottom, y_top = obj.axes.get_ylim()

    y_max = max(y_bottom, y_top)
    y_min = min(y_bottom, y_top)

    ticks: list[Shape] = []

    def ticks_on_right_side() -> bool:
        tick = obj.get_major_ticks()[0]
        return tick.tick2line.get_visible()


    for t in obj.get_major_ticks():
        if t.get_loc() < y_min or t.get_loc() > y_max:
            continue

        tickline = t.tick1line
        char = chr(0x2524)
        if ticks_on_right_side():
            tickline = t.tick2line
            char = chr(0x251C)

        ticks.append(Shape(
            [PointMark(Point(*tickline.get_xydata()[0]), char)],
            [],
            to_mapping(tickline.get_transform().get_affine())
        ))

    label = obj.get_label()
    label_text = label.get_text()
    pos = label.get_position()
    label_tran = label.get_transform()

    tick_labels = obj.get_ticklabels()
    tick_label_elements: list[TextElement] = []

    for tl in tick_labels:
        x,y = tl.get_position()

        if y<y_min or y > y_max:
            continue
        el = TextElement(
            tl.get_text(),
            Point(x,y),
            to_mapping(tl.get_transform()),
            tl.get_horizontalalignment(), # type: ignore
            tl.get_verticalalignment() # type: ignore
        )

        tick_label_elements.append(el)

    axis_label = TextElement(
            label_text,
            Point(*pos),
            to_mapping(label_tran),
            "left" if ticks_on_right_side() else "right",
            "center",
            orientation="vertical"
        )

    return [axis_label] + tick_label_elements + ticks