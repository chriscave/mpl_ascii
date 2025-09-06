from typing import Union, cast
from matplotlib.spines import Spine

from mpl_ascii.artists.transform_helpers import AffineMap, Point, blend_affine_maps, to_mapping
from mpl_ascii.artists.types import LineMark, PointMark, Shape

# chr(0x250C) # ┌
# chr(0x2510) # ┐
# chr(0x250C) # ┌
# chr(0x2510) # ┐

def parse(obj: Spine) -> Union[Shape, None]:

    spty: str = obj.spine_type


    position_type: str = ""
    amount: float = 0.

    # Skip visibility check for colorbar spines - they're always meant to be visible
    # TODO: this should be using a more reliable method than obj.get_visible()
    if not obj.get_visible() and not hasattr(obj.axes, '_colorbar'):
        return


    pos = obj.get_position()

    if isinstance(pos, tuple):
        position_type, amount = obj.get_position()

    if pos == "center":
        position_type, amount = "axes", 0.5

    if pos == "zero":
        position_type, amount = "data", 0.


    if position_type == "outward":

        # Outward points need to be comnverted to pixels to get the right display coordinates.
        amount_px = amount * obj.get_figure().dpi / 72.0

        if spty == "left":
            point_a = Point(0, 0)
            point_b = Point(0, 1)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            mapping_x = AffineMap.identity().translate(Point(-amount_px, 0)) @ mapping_x

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2514)), PointMark(point_b,chr(0x250C))],
                lines = [LineMark(point_a, point_b, chr(0x2502))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "right":
            point_a = Point(1, 0)
            point_b = Point(1, 1)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            mapping_x = AffineMap.identity().translate(Point(-amount_px, 0)) @ mapping_x

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2518)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2502))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "top":
            point_a = Point(0, 1)
            point_b = Point(1, 1)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            mapping_y = AffineMap.identity().translate(Point(0, -amount_px)) @ mapping_y

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x250C)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2500))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "bottom":
            point_a = Point(0, 0)
            point_b = Point(1, 0)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            blended_map = blend_affine_maps(mapping_x, mapping_y)
            m = AffineMap.identity().translate(Point(0, -amount_px)) @ blended_map

            return Shape(
                points = [PointMark(point_a, chr(0x2514)), PointMark(point_b,chr(0x2518))],
                lines = [LineMark(point_a, point_b, chr(0x2500))],
                mapping=m,
                override_zorder=1.
            )

    if position_type == "axes":
        if spty == "left":
            point_a = Point(amount, 0)
            point_b = Point(amount, 1)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2514)), PointMark(point_b,chr(0x250C))],
                lines = [LineMark(point_a, point_b, chr(0x2502))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "right":
            point_a = Point(amount, 0)
            point_b = Point(amount, 1)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2518)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2502))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "top":
            point_a = Point(0, amount)
            point_b = Point(1, amount)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x250C)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2500))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "bottom":
            point_a = Point(0, amount)
            point_b = Point(1, amount)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2514)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2500))],
                mapping=blended_map,
                override_zorder=1.
            )

    if position_type == "data":
        if spty == "left":
            point_a = Point(amount, 0)
            point_b = Point(amount, 1)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transData))


            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2514)), PointMark(point_b,chr(0x250C))],
                lines = [LineMark(point_a, point_b, chr(0x2502))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "right":
            point_a = Point(amount, 0)
            point_b = Point(amount, 1)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transAxes))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transData))


            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2518)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2502))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "top":
            point_a = Point(0, amount)
            point_b = Point(1, amount)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transData))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))


            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x250C)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2500))],
                mapping=blended_map,
                override_zorder=1.
            )

        if spty == "bottom":
            point_a = Point(0, amount)
            point_b = Point(1, amount)

            mapping_y = cast(AffineMap, to_mapping(obj.axes.transData))
            mapping_x = cast(AffineMap, to_mapping(obj.axes.transAxes))

            blended_map = blend_affine_maps(mapping_x, mapping_y)

            return Shape(
                points = [PointMark(point_a, chr(0x2514)), PointMark(point_b,chr(0x2510))],
                lines = [LineMark(point_a, point_b, chr(0x2500))],
                mapping=blended_map,
                override_zorder=1.
            )

    return None