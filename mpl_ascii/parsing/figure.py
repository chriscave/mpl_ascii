
from __future__ import annotations

import os
import importlib.util
from typing import Iterable, Union, cast
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.transforms import Transform
from matplotlib.artist import Artist


from mpl_ascii.artists.transform_helpers import to_mapping
from mpl_ascii.artists.types import Shape, TextElement
from mpl_ascii.parsing.shape import parse_shape, parse_text
from mpl_ascii.parsing.transform import parse_mapping
from mpl_ascii.scene.entities import ParsedFigure, ParsedLineMark, ParsedShape, ParsedText
from mpl_ascii.scene.geometry.point import Point2d
from mpl_ascii.scene.store import Store



def from_figure(figure: Figure, store: Store) -> ParsedFigure:


    figure_transform = cast(Transform, figure.transFigure) # type: ignore

    transform = parse_mapping(to_mapping(figure_transform))

    parsed_shapes: list[ParsedShape] = []

    parsed_texts: list[ParsedText] = []


    for i, c in enumerate(figure.get_children()):
        shapes, texts = parse_artist(c, i)
        parsed_shapes += shapes
        parsed_texts += texts

    for s in parsed_shapes:
        store.add(s)

    for t in parsed_texts:
        store.add(t)


    background_patches = tuple([s.identifier() for s in parsed_shapes if is_backgroud_patch(s, figure)])

    parsed_figure = ParsedFigure(
        figure2display_tranform=transform,
        shapes=tuple(p.identifier() for p in parsed_shapes),
        texts=tuple(t.identifier() for t in parsed_texts),
        background_patches=background_patches
    )

    return parsed_figure

def parse_artist(artist: Artist, insert_order: float) -> tuple[list[ParsedShape], list[ParsedText]]:

    parsed_shapes: list[ParsedShape] = []
    parsed_texts: list[ParsedText] = []
    # print(artist)
    if isinstance(artist, Axes):
        ax = artist

        # This is here because some Annotations do not have the correct scale
        ax.autoscale_view()

        children: list[Artist] = cast(list[Artist], ax.get_children()) # type: ignore


        for j, c in enumerate(children):
            shapes, texts = parse_artist(c, float(f"{int(insert_order)}.{j}"))
            parsed_shapes += shapes
            parsed_texts += texts

        return parsed_shapes, parsed_texts


    cls_name = type(artist).__name__
    path = f"mpl_ascii/artists/{cls_name}.py"
    if not os.path.exists(path):
        return ([],[])


    module_name = path.replace('/', '.')
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return ([],[])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "parse"):
        return ([],[])
    zorder = artist.get_zorder()

    elements = module.parse(artist)

    if not isinstance(elements, Iterable):
        elements = [elements]

    elements = cast(list[Union[Shape, TextElement]], elements)
    for el in elements:
        if isinstance(el, Shape):
            shape = el
            parsed_shape = parse_shape(shape, zorder, insert_order)
            parsed_shapes.append(parsed_shape)

        elif isinstance(el, TextElement): # type: ignore
            text = el
            parsed_text = parse_text(text, zorder, insert_order)
            parsed_texts.append(parsed_text)
        else:
            continue

    return parsed_shapes, parsed_texts

def is_backgroud_patch(shape: ParsedShape, figure: Figure) -> bool:
    figure_transform = parse_mapping(to_mapping(figure.transFigure))

    axes_transforms = [parse_mapping(to_mapping(ax.transAxes)) for ax in figure.get_axes()]

    return (
        is_rectangle(shape) and
            (
                (shape.local2display_transform() == figure_transform)
                or (shape.local2display_transform() in axes_transforms)
        )
    )


def is_rectangle(shape: ParsedShape) -> bool:
    corners = Point2d(0.,0.), Point2d(0.,1.), Point2d(1.,0.), Point2d(1.,1.)
    shape_points = [pm.p for pm in shape.points]
    lines = (
        ParsedLineMark(a=Point2d(0.00, 0.00), b=Point2d(1.00, 0.00), override='─'),
        ParsedLineMark(a=Point2d(0.00, 1.00), b=Point2d(1.00, 1.00), override='─'),
        ParsedLineMark(a=Point2d(0.00, 0.00), b=Point2d(0.00, 1.00), override='│'),
        ParsedLineMark(a=Point2d(1.00, 0.00), b=Point2d(1.00, 1.00), override='│')
    )

    has_corners = all(c in shape_points for c in corners) and len(shape_points) == 4
    has_edges = lines == shape.lines

    return has_corners and has_edges