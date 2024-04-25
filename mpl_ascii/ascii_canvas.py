import numpy as np

from mpl_ascii.overlay import overlay


class AsciiCanvas:
    def __init__(self, array=None) -> None:
        if isinstance(array, AsciiCanvas):
            array = array.array
        self.array = array

    def update(self, other, location=None):
        if self.array is None:
            return other
        res = overlay(self.array, other.array, location[0], location[1])

        return AsciiCanvas(res)

    @property
    def shape(self):
        if self.array is None:
            return (0,0)
        return self.array.shape

    @property
    def debug(self):
        res = np.where(self.array==" ", ".", self.array)
        return AsciiCanvas(res)


    def __str__(self) -> str:
        res = []
        for row in self.array:
            res.append("".join(row.tolist()))

        res = "\n".join(res)
        return res
