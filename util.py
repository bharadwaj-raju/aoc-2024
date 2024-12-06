from dataclasses import dataclass
from math import sqrt
import sys
from pathlib import Path
from typing import Iterable, Literal, Sequence
from itertools import product


def readlines() -> list[str]:
    return Path(sys.argv[1]).read_text().splitlines()


def readtext() -> str:
    return Path(sys.argv[1]).read_text()


def readgrid() -> list[list[str]]:
    return [list(line) for line in readlines()]


def sgn(x: int) -> Literal[-1, 0, +1]:
    if x == 0:
        return 0
    if x < 0:
        return -1
    return +1


@dataclass(frozen=True)
class vec2:
    x: int
    y: int

    @staticmethod
    def xs(vecs: Iterable["vec2"]) -> list[int]:
        return [vec.x for vec in vecs]

    @staticmethod
    def ys(vecs: Iterable["vec2"]) -> list[int]:
        return [vec.y for vec in vecs]

    @staticmethod
    def all_directions() -> list["vec2"]:
        return [vec2(x, y) for x, y in product([+1, -1, 0], repeat=2) if (x, y) != (0, 0)]

    @staticmethod
    def cardinal_directions() -> list["vec2"]:
        return [vec2(x, y) for x, y in ((+1, 0), (-1, 0), (0, -1), (0, +1))]

    def __add__(self, other: "vec2") -> "vec2":
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "vec2") -> "vec2":
        return vec2(self.x - other.x, self.y - other.y)

    def __neg__(self) -> "vec2":
        return vec2(-self.x, -self.y)

    def euclidean(self, other: "vec2") -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def manhattan(self, other: "vec2") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def all_neighbors(self) -> list["vec2"]:
        return [self + delta for delta in vec2.all_directions()]

    def cardinal_neighbors(self) -> list["vec2"]:
        return [self + delta for delta in vec2.cardinal_directions()]


def grid_get(grid: Sequence[Sequence[str]], pos: vec2, default: str = ".") -> str:
    if pos.x < 0 or pos.y < 0:
        return default
    try:
        return grid[pos.y][pos.x]
    except IndexError:
        return default
