from collections import defaultdict
from collections.abc import Sequence
from util import grid_get, vec2, readgrid

grid = readgrid()

sym2dir = {
    "^": vec2(0, -1),
    "<": vec2(-1, 0),
    ">": vec2(+1, 0),
    "v": vec2(0, +1),
}

turn_right_90 = {"^": ">", ">": "v", "v": "<", "<": "^"}


def walk(grid: Sequence[Sequence[str]], guard: vec2, facing: str) -> list[vec2]:
    path: list[vec2] = [guard]
    while True:
        in_front = grid_get(grid, guard + sym2dir[facing], default="O")
        if in_front == "O":
            break
        if in_front == "#":
            facing = turn_right_90[facing]
        guard = guard + sym2dir[facing]
        path.append(guard)
    return path


guard = None
facing = None

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell in {"^", "<", ">", "v"}:
            guard = vec2(x, y)
            facing = cell

assert guard is not None
assert facing is not None

print(len(set(walk(grid, guard, facing))))
