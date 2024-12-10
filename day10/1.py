from functools import reduce
from util import vec2, readgrid, grid_get

grid = readgrid()


def score(grid: list[list[str]], start: vec2) -> set[vec2]:
    curr = grid_get(grid, start, "-10")
    if curr == "8":
        return set(nb for nb in start.cardinal_neighbors() if grid_get(grid, nb) == "9")
    return reduce(
        set.union,
        (score(grid, nb) for nb in start.cardinal_neighbors() if grid_get(grid, nb) == str(int(curr) + 1)),
        set(),
    )


scoresum = 0

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "0":
            sc = score(grid, vec2(x, y))
            scoresum += len(sc)

print(scoresum)
