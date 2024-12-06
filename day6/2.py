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


def causes_loop(
    grid: Sequence[Sequence[str]], guard: vec2, facing: str, obstacle: vec2
) -> bool:
    turn_facings: defaultdict[vec2, set[str]] = defaultdict(set)
    while True:
        in_front_pos = guard + sym2dir[facing]
        in_front = grid_get(grid, in_front_pos, default="O")
        if in_front == "O":
            break
        if in_front == "#" or in_front_pos == obstacle:
            if facing in turn_facings[in_front_pos]:
                return True
            turn_facings[in_front_pos].add(facing)
            while (
                grid_get(grid, guard + sym2dir[facing], default="O") == "#"
                or guard + sym2dir[facing] == obstacle
            ):
                facing = turn_right_90[facing]
        guard = guard + sym2dir[facing]
    return False


guard = None
facing = None

obstacles = set()
possible_y = set()
possible_x = set()

rows = len(grid)
cols = len(grid[0])

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell in {"^", "<", ">", "v"}:
            guard = vec2(x, y)
            facing = cell
        elif cell == "#":
            if x + 1 < cols:
                possible_x.add(x + 1)
            if x - 1 >= 0:
                possible_x.add(x - 1)
            if y + 1 < rows:
                possible_y.add(y + 1)
            if y - 1 >= 0:
                possible_y.add(y - 1)
            obstacles.add(vec2(x, y))

assert guard is not None
assert facing is not None

normal_path = walk(grid, guard, facing)

looping_obstacles = set()

for would_step in normal_path[1:]:
    if causes_loop(grid, guard, facing, would_step):
        looping_obstacles.add(would_step)

print(len(looping_obstacles))
