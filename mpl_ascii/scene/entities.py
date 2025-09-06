from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Literal, Union

from matplotlib.colors import to_rgba

from mpl_ascii.scene.fingerprint import Fingerprintable, combine, f8
from mpl_ascii.scene.geometry.affine import AffineMap2d
from mpl_ascii.scene.geometry.point import Point2d


@dataclass(frozen=True)
class ParsedColor(Fingerprintable):
    red: float
    green: float
    blue: float
    alpha: float

    def fingerprint(self) -> bytes:
        return f"color({f8(self.red)},{f8(self.green)},{f8(self.blue)},{f8(self.alpha)})".encode()

    @property
    def hex_color_with_alpha(self) -> str:
        r = int(self.red * 255)
        g = int(self.green * 255)
        b = int(self.blue * 255)
        a = int(self.alpha * 255)
        return "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

    @property
    def hex_color(self) -> str:
        return self.to_hex(self.red, self.green, self.blue)

    @staticmethod
    def to_hex(r: float,g: float, b:float) -> str:
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    @classmethod
    def from_hex(cls, hex: str) -> ParsedColor:
        return cls(*to_rgba(hex))

    def __repr__(self) -> str:
        return self.hex_color_with_alpha

@dataclass(frozen=True)
class ParsedColorMap(Fingerprintable):
    _call: Callable[[float], ParsedColor]

    def fingerprint(self) -> bytes:
        sample_points = [0.0, 0.25, 0.5, 0.75, 1.0]
        parts: list[bytes] = []
        for x in sample_points:
            color = self(x)
            parts.append(f"s({f8(x)}):{color.fingerprint().decode()}".encode())
        return f"cmap({','.join(p.decode() for p in parts)})".encode()

    def approx_inverse(self, target_color: ParsedColor, resolution: int = 10) -> float:
        min_distance = float('inf')
        best_x = 0.0

        for i in range(resolution + 1):
            x = i / resolution
            color = self(x)

            # Calculate Euclidean distance in RGB space
            distance = (
                (color.red - target_color.red) ** 2 +
                (color.green - target_color.green) ** 2 +
                (color.blue - target_color.blue) ** 2
            ) ** 0.5

            if distance < min_distance:
                min_distance = distance
                best_x = x

        return best_x

    def __call__(self, x: float) -> ParsedColor:
        return self._call(x)




@dataclass(frozen=True)
class StyleContext(Fingerprintable):
    point_color: Union[ParsedColor, None]
    line_color: Union[ParsedColor, None]
    fill_color: Union[ParsedColor, None]
    line_width: Union[float, None]


    def fingerprint(self) -> bytes:
        parts: list[bytes] = [b"ptc()", b"lc()", b"fc()", b"lw()", b"cmap()"]
        if self.point_color:
            parts[0] = b"ptc(" +self.point_color.fingerprint() + b")"
        if self.line_color:
            parts[1] = b"lc(" +self.line_color.fingerprint() + b")"

        if self.fill_color:
            parts[2] = b"fc(" +self.fill_color.fingerprint() + b")"

        if self.line_width:
            parts[3] = f"lw({self.line_width})".encode()

        parts_str = [p.decode() for p in parts]
        return f"stylectx({','.join(parts_str)})".encode()

class Identifable(ABC):

    @abstractmethod
    def identifier(self) -> str:
        raise NotImplementedError()

class TransformAware(ABC):

    @abstractmethod
    def local2display_transform(self) -> AffineMap2d:
        raise NotImplementedError()


@dataclass(frozen=True)
class ParsedPointMark(Fingerprintable):
    p: Point2d
    override: Union[str, None]
    color: Union[ParsedColor, None]

    def fingerprint(self) -> bytes:
        override = f"ov({self.override})" if self.override else "ov()"
        return f"ppm({self.p.fingerprint().decode()}, {override})".encode()

    def __repr__(self) -> str:
        return f"{self.p}, {self.override}"

@dataclass(frozen=True)
class ParsedLineMark(Fingerprintable):
    a: Point2d
    b: Point2d
    override: Union[str, None]

    def fingerprint(self) -> bytes:
        override = f"ov({self.override})" if self.override else "ov()"
        return f"plm({self.a.fingerprint().decode(), self.b.fingerprint().decode(), override})".encode()

@dataclass(frozen=True)
class ParsedShape(Identifable, Fingerprintable, TransformAware):
    id: str = field(init=False)
    points: tuple[ParsedPointMark,...]
    lines: tuple[ParsedLineMark,...]
    style_context: StyleContext
    zorder: float
    transform2display: AffineMap2d
    insert_order: float

    def __post_init__(self):

        parts: list[bytes] = []

        for p in self.points:
            parts.append(p.fingerprint())
        for lm in self.lines:
            parts.append(lm.fingerprint())

        parts.append(self.style_context.fingerprint())
        parts.append(f"z({f8(self.zorder)})".encode())
        parts.append(self.transform2display.fingerprint())
        parts.append(f"io({self.insert_order})".encode())


        fid = combine(parts)[:8]
        object.__setattr__(self, "id", f"shape:{fid}")


    def fingerprint(self) -> bytes:
        return self.identifier().encode()

    def identifier(self) -> str:
        return self.id

    def local2display_transform(self) -> AffineMap2d:
        return self.transform2display

@dataclass(frozen=True)
class ParsedFigure(Identifable, Fingerprintable, TransformAware):
    id: str = field(init=False)
    figure2display_tranform: AffineMap2d
    shapes: tuple[str,...]
    texts: tuple[str,...]
    background_patches: tuple[str,...]

    def __post_init__(self):
        parts: list[bytes] = []

        for s_id in self.shapes:
            parts.append(s_id.encode())

        for t_id in self.texts:
            parts.append(t_id.encode())

        for b_id in self.background_patches:
            parts.append(b_id.encode())

        parts.append(self.figure2display_tranform.fingerprint())
        fid = combine(parts)[:8]
        object.__setattr__(self, "id", f"fig:{fid}")


    def fingerprint(self) -> bytes:
        return self.identifier().encode()

    def identifier(self) -> str:
        return self.id

    def local2display_transform(self) -> AffineMap2d:
        return self.figure2display_tranform

@dataclass(frozen=True)
class ParsedText(Identifable, Fingerprintable, TransformAware):
    id: str = field(init=False)
    text: str
    anchor: Point2d
    orientation: Literal["horizontal", "vertical"]
    horizontal_alignment: Literal["left", "center", "right"]
    vertical_alignment: Literal["top", "center_baseline", "center", "baseline", "bottom"]
    zorder: float
    transform2display: AffineMap2d
    insert_order: float

    def __post_init__(self):
        parts: list[bytes] = []

        parts.append(self.text.encode())
        parts.append(self.anchor.fingerprint())
        parts.append(f"halign({self.horizontal_alignment})".encode())
        parts.append(f"valign({self.vertical_alignment})".encode())
        parts.append(f"z({f8(self.zorder)})".encode())
        parts.append(self.transform2display.fingerprint())
        parts.append(f"io({self.insert_order})".encode())
        parts.append(f"orientation({self.orientation})".encode())


        fid = combine(parts)[:8]
        object.__setattr__(self, "id", f"text:{fid}")


    def fingerprint(self) -> bytes:
        return self.identifier().encode()

    def identifier(self) -> str:
        return self.id

    def local2display_transform(self) -> AffineMap2d:
        return self.transform2display

