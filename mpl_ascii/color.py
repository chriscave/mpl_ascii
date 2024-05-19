
import matplotlib


def std_color(color):
    return matplotlib.colors.to_hex(color)


class Char:
    def __init__(self, character: str, color: str) -> None:
        self.character=character
        self.color=color

    def __str__(self) -> str:
        return self.character


    def __rich__(self) -> str:
        return f"[{self.color}]{self.character}[/{self.color}]"