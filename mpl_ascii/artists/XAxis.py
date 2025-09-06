from __future__ import annotations
from typing import Union
from matplotlib.axis import XAxis

from mpl_ascii.artists.transform_helpers import Point, to_mapping
from mpl_ascii.artists.types import PointMark, Shape, TextElement



def parse(obj: XAxis) -> list[Union[Shape, TextElement]]:

    x_left, x_right = obj.axes.get_xlim()

    x_max = max(x_left, x_right)
    x_min = min(x_left, x_right)

    ticks: list[Shape] = []

    for t in obj.get_major_ticks():

        if t.get_loc() < x_min or t.get_loc() > x_max:
            continue


        tickline = t.tick1line or t.tick2line
        ticks.append(Shape(
            [PointMark(Point(t.get_loc(), 0), chr(0x252C))],
            [],
            to_mapping(tickline.get_transform().get_affine())
        ))

    label = obj.get_label()
    label_text = label.get_text()
    pos = label.get_position()
    label_tran = label.get_transform()


    halign = label.get_horizontalalignment()
    valign = label.get_verticalalignment()

    tick_labels = obj.get_ticklabels()
    tick_label_elements: list[TextElement] = []
    for tl in tick_labels:
        x,y = tl.get_position()
        if x<x_min or x > x_max:
            continue

        el = TextElement(
            tl.get_text(),
            Point(x,y),
            to_mapping(tl.get_transform()),
            tl.get_horizontalalignment(), # type: ignore
            tl.get_verticalalignment() # type: ignore
        )
        tick_label_elements.append(el)

    return [
        TextElement(
            label_text,
            Point(*pos),
            to_mapping(label_tran),
            halign, # type: ignore
            valign, # type: ignore
        )
    ] + tick_label_elements + ticks