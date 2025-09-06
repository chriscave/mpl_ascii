from __future__ import annotations
from dataclasses import dataclass
from typing import Union

from mpl_ascii.layout.rasterize import rasterize_line, scanline_fill
from mpl_ascii.layout.discrete_point import DiscretePoint
from mpl_ascii.scene.entities import ParsedLineMark, ParsedPointMark, ParsedShape
from mpl_ascii.scene.fingerprint import combine
from mpl_ascii.scene.geometry.affine import AffineMap2d


@dataclass
class Vertex:
    id: str
    p: DiscretePoint

    @staticmethod
    def id_from_point_mark(pm: ParsedPointMark):
        parts: list[bytes] = []
        parts.append(pm.fingerprint())
        return f"v:{combine(parts)[:8]}"
@dataclass
class Edge:
    id: str
    a: DiscretePoint
    b: DiscretePoint
    raster_points: list[DiscretePoint]

    @staticmethod
    def id_from_line_mark(lm: ParsedLineMark):
        parts: list[bytes] = []
        parts.append(lm.fingerprint())
        return f"e:{combine(parts)[:8]}"

@dataclass
class FillPoint:
    id: str
    p: DiscretePoint


@dataclass
class ShapeLayout:
    id2obj: dict[str, Union[Vertex, Edge, FillPoint]]

    def add(self, obj: Union[Vertex, Edge, FillPoint]) -> ShapeLayout:
        self.id2obj[obj.id] = obj
        return self

    def get(self, ident: str) -> Union[Vertex, Edge, FillPoint]:
        obj = self.id2obj[ident]
        return obj

    def get_all_vertices(self) -> list[Vertex]:
        vertices: list[Vertex] = []
        for _,v in self.id2obj.items():
            if isinstance(v, Vertex):
                vertices.append(v)

        return vertices

    def get_all_edges(self) -> list[Edge]:
        edges: list[Edge] = []
        for _,e in self.id2obj.items():
            if isinstance(e, Edge):
                edges.append(e)

        return edges

    def get_all_fill(self) -> list[FillPoint]:
        fill_points: list[FillPoint] = []
        for _,fp in self.id2obj.items():
            if isinstance(fp, FillPoint):
                fill_points.append(fp)

        return fill_points


    @classmethod
    def empty(cls):
        return cls({})


def layout_shape(shape: ParsedShape, T: AffineMap2d) -> ShapeLayout:
    shape_layout = ShapeLayout.empty()

    vertices: list[str] = []
    edges: list[str] = []
    fill_vertices: list[str] = []
    for pm in shape.points:
        dp = DiscretePoint.from_point2d(T(pm.p))
        ident = Vertex.id_from_point_mark(pm)
        shape_layout.add(Vertex(ident, dp))
        vertices.append(ident)


    for lm in shape.lines:
        a, b = (DiscretePoint.from_point2d(T(lm.a)), DiscretePoint.from_point2d(T(lm.b)))
        raster_points = rasterize_line(a, b)
        ident = Edge.id_from_line_mark(lm)
        shape_layout.add(Edge(ident, a, b, raster_points))
        edges.append(ident)


    fill_color = shape.style_context.fill_color
    fill_points: list[DiscretePoint] = []
    if fill_color:
        all_vertices = shape_layout.get_all_vertices()
        all_edges = shape_layout.get_all_edges()
        fill_points = scanline_fill([v.p for v in all_vertices], [(e.a, e.b) for e in all_edges])

    for i, p in enumerate(fill_points):
        ident = f"fill_color_{i}"
        shape_layout.add(FillPoint(ident, p))
        fill_vertices.append(ident)

    return shape_layout
