from dataclasses import dataclass
from math import sqrt
import sys
from pathlib import Path
from typing import Iterable, Literal, Sequence
from itertools import cycle, islice, product


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


# from https://docs.python.org/3/library/itertools.html#itertools-recipes, "roundrobin"
def interleave(*iterables):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)


class Node[T]:
    def __init__(self, x: T, prev: "Node[T] | None" = None, next: "Node[T] | None" = None) -> None:
        self.x = x
        self.prev = prev
        self.next = next

    def insert_after(self, x: T) -> "Node[T]":
        old_next = self.next
        self.next = Node(x, prev=self, next=old_next)
        if old_next:
            old_next.prev = self.next
        return self.next

    def insert_before(self, x: T) -> "Node[T]":
        old_prev = self.prev
        self.prev = Node(x, prev=old_prev, next=self)
        if old_prev:
            old_prev.next = self.prev
        return self.prev

    def remove(self) -> None:
        match (self.prev, self.next):
            case (None, None):
                return
            case (p, None):
                p.next = None
            case (None, n):
                n.prev = None
            case (p, n):
                n.prev = p
                p.next = n

    def __iter__(self):
        return NodeIterator(self)


class NodeIterator[T]:
    def __init__(self, head: Node[T] | None = None) -> None:
        self.curr = head

    def __iter__(self):
        return NodeIterator(self.curr)

    def __next__(self) -> Node[T]:
        if not self.curr:
            raise StopIteration
        x = self.curr
        self.curr = self.curr.next
        return x
