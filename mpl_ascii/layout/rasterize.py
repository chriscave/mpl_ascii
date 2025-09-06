from __future__ import annotations
from dataclasses import dataclass

from mpl_ascii.layout.discrete_point import DiscretePoint

@dataclass
class EdgeInfo:
    y_max: int
    x_of_y_min: float
    slope_inverse: float


def scanline_fill(vertices: list[DiscretePoint], edges: list[tuple[DiscretePoint, DiscretePoint]]) -> list[DiscretePoint]:

    all_edge_points = {p for e in edges for p in rasterize_line(e[0], e[1])}

    if not vertices:
        return []

    vertices = sorted(vertices, key=lambda p: p.y)
    y_min = vertices[0].y
    y_max = vertices[-1].y

    # Step 1: Build Edge Table
    edge_table: dict[int, list[EdgeInfo]] = {}

    for edge in edges:
        p1, p2 = edge

        # Skip horizontal edges
        if p1.y == p2.y:
            continue

        # Make sure p1 is the lower point (smaller y)
        if p1.y > p2.y:
            p1, p2 = p2, p1

        y_min_edge = p1.y
        y_max_edge = p2.y
        x_of_y_min = p1.x

        # Calculate inverse slope (dx/dy)
        if p2.y - p1.y != 0:  # Should never be 0 due to horizontal edge check
            slope_inverse = (p2.x - p1.x) / (p2.y - p1.y)
        else:
            continue

        edge_info = EdgeInfo(y_max_edge, x_of_y_min, slope_inverse)

        # Add edge to edge table at its y_min
        if y_min_edge not in edge_table:
            edge_table[y_min_edge] = []
        edge_table[y_min_edge].append(edge_info)


    active_list: list[EdgeInfo] = []
    fill: list[DiscretePoint] = []

    for y in range(y_min, y_max):
        # Step 3: Add new edges from edge table to active list
        if y in edge_table:
            active_list.extend(edge_table[y])

        # Step 4: Remove completed edges (yMax <= current y)
        active_list = [edge for edge in active_list if edge.y_max > y]

        # Step 5: Sort active list by x_of_y_min
        active_list.sort(key=lambda edge: edge.x_of_y_min)

        # Step 6: Fill between pairs of edges
        for i in range(0, len(active_list) - 1, 2):
            if i + 1 < len(active_list):
                x_start = int(round(active_list[i].x_of_y_min))
                x_end = int(round(active_list[i + 1].x_of_y_min))

                # Fill pixels between the edges
                for x in range(x_start+1, x_end):
                    fp = DiscretePoint(x, y)
                    if fp in all_edge_points: # Ensure fill is not overwriting edge points
                        continue
                    fill.append(DiscretePoint(x, y))

        # Step 7: Update x_of_y_min for next scanline
        for edge in active_list:
            edge.x_of_y_min += edge.slope_inverse

    return fill


def rasterize_lines(lines: list[tuple[DiscretePoint, DiscretePoint]]) -> list[DiscretePoint]:

    discrete_lines: list[DiscretePoint] = []

    for line in lines:
        discrete_lines += bresenham_line(line[0], line[1])

    return discrete_lines

def rasterize_line(a: DiscretePoint, b: DiscretePoint) -> list[DiscretePoint]:

    return bresenham_line(a, b)



def bresenham_line(p: DiscretePoint, q: DiscretePoint) -> list[DiscretePoint]:
    x0, y0 = p.x, p.y
    x1, y1 = q.x, q.y

    dx = x1 - x0
    dy = y1 - y0

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line if it's steep
    if is_steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    # Swap start and end points if necessary
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # Recalculate differences
    dx = x1 - x0
    dy = y1 - y0

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y0 < y1 else -1

    # Iterate over bounding box generating points between start and end
    y = y0
    points: list[DiscretePoint] = []
    for x in range(x0, x1 + 1):
        coord = DiscretePoint(y, x) if is_steep else DiscretePoint(x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    return [point for point in points if point != p and point != q]
