from functools import reduce
from util import vec2, readgrid, grid_get

grid = readgrid()


def rating(grid: list[list[str]], start: vec2) -> int:
    curr = grid_get(grid, start, "-10")
    if curr == "8":
        return sum(grid_get(grid, nb) == "9" for nb in start.cardinal_neighbors())
    return sum(rating(grid, nb) for nb in start.cardinal_neighbors() if grid_get(grid, nb) == str(int(curr) + 1))


ratingsum = 0

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "0":
            ra = rating(grid, vec2(x, y))
            ratingsum += ra

print(ratingsum)
