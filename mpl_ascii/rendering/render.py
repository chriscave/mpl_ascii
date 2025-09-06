
from __future__ import annotations
from mpl_ascii.layout.layout_text import layout_text
from mpl_ascii.presentation.glyphs import Glyph, PointGlyph, resolve_glyphs
from mpl_ascii.layout.layout_shape import Edge, FillPoint, ShapeLayout, Vertex, layout_shape
from mpl_ascii.presentation.visibility import decide_visibility
from mpl_ascii.scene.geometry.affine import AffineMap2d
from mpl_ascii.scene.geometry.matrix import Matrix2d
from mpl_ascii.scene.geometry.point import Point2d
from mpl_ascii.rendering.canvas import AsciiCanvas, Renderable, RenderableElement
from mpl_ascii.layout.render_plan import CharMap
from mpl_ascii.scene.entities import ParsedFigure, ParsedShape, ParsedText
from mpl_ascii.scene.store import Store
from mpl_ascii.presentation.color_policy import qualify_for_display


def draw_shape(resolved_glyphs: dict[str, Glyph], shape_layout: ShapeLayout):
    point_glyphs2: list[PointGlyph] = []
    for ident, glyph in resolved_glyphs.items():
        shape_element = shape_layout.get(ident)
        if isinstance(shape_element, Vertex) or isinstance(shape_element, FillPoint):
            point_glyphs2.append(PointGlyph(shape_element.p, glyph))
        elif isinstance(shape_element, Edge): # type: ignore
            point_glyphs2 += [PointGlyph(rp, glyph) for rp in shape_element.raster_points]

    return RenderableElement(point_glyphs2)


def draw_figure(
        figure: ParsedFigure,
        ascii_canvas_height: int,
        ascii_canvas_width: int,
        store: Store,
    ) -> AsciiCanvas:

    renderable_objs: list[tuple[Renderable, float, float]] = []

    char_map = CharMap.empty()

    M = Matrix2d(ascii_canvas_width-1, 0,0,ascii_canvas_height-1)

    figure2ascii_canvas_transform = AffineMap2d(M, Point2d(0,0))
    display2figure_transform = figure.figure2display_tranform.inverse()

    for shape_id in figure.shapes:

        if shape_id in figure.background_patches:
            continue

        parsed_shape = store.get(shape_id, ParsedShape)
        transform = figure2ascii_canvas_transform @ display2figure_transform @ parsed_shape.local2display_transform()

        shape_layout = layout_shape(parsed_shape, transform)
        dc = qualify_for_display(parsed_shape)
        vis = decide_visibility(parsed_shape, dc)
        id2glyph = resolve_glyphs(parsed_shape, vis, dc, char_map, shape_layout)
        renderable_shape = draw_shape(id2glyph, shape_layout)

        renderable_objs.append(
                (renderable_shape, parsed_shape.zorder, parsed_shape.insert_order)
            )

    for ident in figure.texts:

        text = store.get(ident, ParsedText)
        transform = figure2ascii_canvas_transform @ display2figure_transform @ text.local2display_transform()

        points = layout_text(text, transform, ascii_canvas_height, ascii_canvas_width)

        renderable_objs.append((RenderableElement(points), text.zorder, text.insert_order))

    canvas = AsciiCanvas.initialise(ascii_canvas_height, ascii_canvas_width)


    renderable_objs = sorted(renderable_objs, key=lambda x: (x[1], x[2]))
    for obj, _, _ in renderable_objs:
        obj.render(canvas)


    return canvas
