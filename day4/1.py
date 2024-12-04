from itertools import product
from typing import Iterable
from util import readlines, vec2, grid_get

puzzle = readlines()
rows = len(puzzle)
cols = len(puzzle[0])


def check_in_direction(
    puzzle: list[str], pos: vec2, delta: vec2, needle: Iterable[str]
) -> bool:
    cumulative_delta = delta
    for rem in needle:
        if grid_get(puzzle, pos + cumulative_delta) == rem:
            cumulative_delta += delta
        else:
            break
    else:
        return True
    return False


found = 0

for y in range(rows):
    for x in range(cols):
        pos = vec2(x, y)
        if grid_get(puzzle, pos) == "X":
            for delta in vec2.all_directions():
                if check_in_direction(puzzle, pos, delta, "MAS"):
                    found += 1

print(found)
