from mpl_ascii.artists.transform_helpers import AffineMap, Mapping
from mpl_ascii.scene.geometry.affine import AffineMap2d
from mpl_ascii.scene.geometry.matrix import Matrix2d
from mpl_ascii.scene.geometry.point import Point2d


def parse_mapping(mapping: Mapping) -> AffineMap2d:

    if isinstance(mapping, AffineMap):
        mat = Matrix2d(mapping.linear.a, mapping.linear.b, mapping.linear.c, mapping.linear.d)
        p = Point2d(mapping.translation.x, mapping.translation.y)
        return AffineMap2d(mat, p)

