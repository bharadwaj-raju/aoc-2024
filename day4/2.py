from collections.abc import Iterable
from util import readlines, vec2, grid_get

puzzle = readlines()
rows = len(puzzle)
cols = len(puzzle[0])


def check_in_direction_full(puzzle: list[str], pos: vec2, delta: vec2, needle: Iterable[str]) -> bool:
    cumulative_delta = vec2(0, 0)
    for rem in needle:
        if rem == "." or grid_get(puzzle, pos + cumulative_delta) == rem:
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
        if any(check_in_direction_full(puzzle, pos, vec2(+1, +1), v) for v in ("MAS", "SAM")):
            if any(check_in_direction_full(puzzle, pos + vec2(+2, +0), vec2(-1, +1), v) for v in ("MAS", "SAM")):
                found += 1

print(found)
