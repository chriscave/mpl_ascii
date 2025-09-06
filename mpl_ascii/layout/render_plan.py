from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator
from mpl_ascii.layout.constants import RESERVED_CHARS


@dataclass
class CharGenerator:
    exclude: set[str] = field(default_factory=lambda: RESERVED_CHARS)
    _chars: list[str] = field(init=False)
    _index: int = field(init=False, default=0)

    def __post_init__(self):
        ascii_range = [chr(i) for i in range(33, 127)]  # Printable ASCII
        self._chars = [c for c in ascii_range if c not in self.exclude]

        if not self._chars:
            raise ValueError("No characters available for generation.")

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if not self._chars:
            raise StopIteration

        char = self._chars[self._index]
        self._index = (self._index + 1) % len(self._chars)
        return char

@dataclass
class CharMap:
    color2char: dict[str, str]
    char_generator: CharGenerator


    @classmethod
    def empty(cls):
        return cls({}, CharGenerator())

    def resolve_char(self, hex_color: str) -> str:
        if hex_color not in self.color2char:
            self.color2char[hex_color] = next(self.char_generator)
        return self.color2char[hex_color]

    def get_char2color(self) -> dict[str, str]:
        return {char: color for color, char in self.color2char.items()}


@dataclass
class CharResolver:
    point_char_map: CharMap = field(init=False)
    lines_char_map: CharMap = field(init=False)
    fill_char_map: CharMap = field(init=False)

