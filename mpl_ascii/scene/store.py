from __future__ import annotations

from dataclasses import dataclass
from typing import Type, TypeVar

from mpl_ascii.scene.entities import Identifable

T = TypeVar("T")

@dataclass
class Store:
    id2obj: dict[str, Identifable]

    @classmethod
    def empty(cls) -> Store:
        return Store({})

    def add(self, obj: Identifable) -> Store:
        self.id2obj[obj.identifier()] = obj
        return self

    def get(self, ident: str, ttype: Type[T]) -> T:
        obj = self.id2obj[ident]
        if not isinstance(obj, ttype):
            raise TypeError(f"{ident} is not of type {ttype.__name__}")
        return obj


