from collections import defaultdict
from collections.abc import Iterable, Sequence
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
    grid: Sequence[Sequence[str]],
    guard: vec2,
    facing: str,
    obstacle: vec2,
    obstacles_by_row: dict[int, list[int]],
    obstacles_by_col: dict[int, list[int]],
) -> bool:
    seen = {(guard, facing)}
    while True:
        next_x, next_y = guard.x, guard.y
        try:
            if facing == "^":
                next_y = max(y for y in obstacles_by_col[guard.x] if y < guard.y)
            elif facing == ">":
                next_x = min(x for x in obstacles_by_row[guard.y] if x > guard.x)
            elif facing == "<":
                next_x = max(x for x in obstacles_by_row[guard.y] if x < guard.x)
            elif facing == "v":
                next_y = min(y for y in obstacles_by_col[guard.x] if y > guard.y)
        except ValueError:
            break
        guard = vec2(next_x, next_y)
        curr = grid_get(grid, guard, default="O")
        if curr == "O":
            break
        if curr == "#" or guard == obstacle:
            guard = guard - sym2dir[facing]
            while grid_get(grid, guard + sym2dir[facing], default="O") == "#" or guard + sym2dir[facing] == obstacle:
                facing = turn_right_90[facing]
                if (guard, facing) in seen:
                    return True
        if (guard, facing) in seen:
            return True
        seen.add((guard, facing))
    return False


guard = None
facing = None

obstacles_by_row: defaultdict[int, list[int]] = defaultdict(list)
obstacles_by_col: defaultdict[int, list[int]] = defaultdict(list)

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell in {"^", "<", ">", "v"}:
            guard = vec2(x, y)
            facing = cell
        elif cell == "#":
            obstacles_by_row[y].append(x)
            obstacles_by_col[x].append(y)

assert guard is not None
assert facing is not None

normal_path = walk(grid, guard, facing)

looping_obstacles = set()

for would_step in set(normal_path[1:]):
    obstacles_by_col[would_step.x].append(would_step.y)
    obstacles_by_row[would_step.y].append(would_step.x)
    if causes_loop(grid, guard, facing, would_step, obstacles_by_row, obstacles_by_col):
        looping_obstacles.add(would_step)
    obstacles_by_col[would_step.x].pop()
    obstacles_by_row[would_step.y].pop()

print(len(looping_obstacles))
