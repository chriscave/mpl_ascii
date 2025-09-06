from mpl_ascii.presentation.glyphs import Glyph, PointGlyph
from mpl_ascii.layout.discrete_point import DiscretePoint
from mpl_ascii.scene.entities import ParsedText
from mpl_ascii.scene.geometry.affine import AffineMap2d


def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(v, hi))

def layout_horiztonal_text(parsed_text: ParsedText, anchor: DiscretePoint, canvas_height: int, canvas_width: int) -> list[PointGlyph]:
    W, H = canvas_width, canvas_height
    L = len(parsed_text.text)

    # start from anchor
    x, y = anchor.x, anchor.y

    direction = "right"

    # --- horizontal alignment ---
    if parsed_text.horizontal_alignment == "left":
        direction = "right"
        x = clamp(x + 1, 0, max(W - 1, 0))  # keep full text on canvas when drawing → right

    elif parsed_text.horizontal_alignment == "right":
        direction = "left"
        # when drawing ← left, the starting x must be at least L-1 to keep full text on
        lo = min(L - 1, W - 1)
        x = clamp(x - 1, lo, W - 1)

    elif parsed_text.horizontal_alignment == "center":
        direction = "right"
        x = clamp(x - (L // 2), 0, max(W - L, 0))

    # --- vertical alignment ---

    if parsed_text.vertical_alignment == "top":
        y = clamp(y - 1, 0, H - 1)
    elif parsed_text.vertical_alignment in ("center_baseline", "center"):
        y = clamp(y + 0, 0, H - 1)
    elif parsed_text.vertical_alignment in ("baseline", "bottom"):
        y = clamp(y + 1, 0, H - 1)

    point_glyphs: list[PointGlyph] = []

    if direction == "right":
        for i, char in enumerate(parsed_text.text):
            dp = DiscretePoint(x+i, y)
            point_glyphs.append(PointGlyph(dp, Glyph(char, None)))

    if direction == "left":
        for i, char in enumerate(reversed(parsed_text.text)):
            dp = DiscretePoint(x-i, y)
            point_glyphs.append(PointGlyph(dp, Glyph(char, None)))

    return point_glyphs


def layout_vertical_text(parsed_text: ParsedText, anchor: DiscretePoint, canvas_height: int, canvas_width: int) -> list[PointGlyph]:
    W, H = canvas_width, canvas_height
    L = len(parsed_text.text)

    # start from anchor
    x, y = anchor.x, anchor.y

    direction = "down"
    if parsed_text.horizontal_alignment == "left":
        x = clamp(x + 1, 0, W - 1)   # anchor is left of text → draw one col to the right
    elif parsed_text.horizontal_alignment == "right":
        x = clamp(x - 1, 0, W - 1)   # anchor is right of text → draw one col to the left
    elif parsed_text.horizontal_alignment == "center":
        x = clamp(x + 0, 0, W - 1)   # same column

    if parsed_text.vertical_alignment == "top":
        direction = "down"
        y = clamp(y + 1, 0, max(H - 1, 0))          # draw ↓ from just below anchor
    elif parsed_text.vertical_alignment in ("center_baseline", "center"):
        direction = "down"
        y = clamp(y + (L // 2), 0, max(H - 1, 0))   # center the run around anchor

    elif parsed_text.vertical_alignment in ("baseline", "bottom"):
        direction = "up"
        lo = min(L - 1, H - 1)                      # need at least L-1 rows above
        y = clamp(y - 1, lo, H - 1)


    point_glyphs: list[PointGlyph] = []

    if direction == "down":
        for i, char in enumerate(parsed_text.text):
            dp = DiscretePoint(x, y-i)
            point_glyphs.append(PointGlyph(dp, Glyph(char, None)))

    if direction == "up":
        for i, char in enumerate(reversed(parsed_text.text)):
            dp = DiscretePoint(x, y+i)
            point_glyphs.append(PointGlyph(dp, Glyph(char, None)))

    return point_glyphs


def layout_text(text: ParsedText, T: AffineMap2d, canvas_height: int, canvas_width: int) -> list[PointGlyph]:

    anchor = DiscretePoint.from_point2d(T(text.anchor))

    glyphs: list[PointGlyph] = []

    if text.orientation == "horizontal":
        glyphs = layout_horiztonal_text(text, anchor, canvas_height, canvas_width)

    if text.orientation == "vertical":
        glyphs = layout_vertical_text(text, anchor, canvas_height, canvas_width)

    return glyphs
