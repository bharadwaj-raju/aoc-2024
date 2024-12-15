from util import readtext, grid_get, vec2

grid, movements = readtext().split("\n\n")
grid = [list(row) for row in grid.splitlines()]
movements = movements.replace("\n", "")

sym2dir = {
    "^": vec2(+0, -1),
    ">": vec2(+1, +0),
    "v": vec2(+0, +1),
    "<": vec2(-1, +0),
}

movements = [sym2dir[s] for s in movements]

robot = None
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "@":
            robot = vec2(x, y)
            grid[y][x] = "."
assert robot is not None

type Grid = list[list[str]]


def push(grid: Grid, box: vec2, dir: vec2) -> bool:
    in_front = grid_get(grid, box + dir, default="#")
    if in_front == ".":
        grid[box.y][box.x] = "."
        grid[(box + dir).y][(box + dir).x] = "O"
        return True
    elif in_front == "#":
        return False
    elif in_front == "O":
        if push(grid, box + dir, dir):
            grid[box.y][box.x] = "."
            grid[(box + dir).y][(box + dir).x] = "O"
            return True
        else:
            return False
    raise ValueError(f"unknown cell value {in_front}")


for move in movements:
    # print("\n".join("".join(cell for cell in row) for row in grid))
    in_front = grid_get(grid, robot + move, default="#")
    if in_front == ".":
        robot += move
    elif in_front == "O":
        if push(grid, robot + move, move):
            robot += move
    else:
        pass

coordsum = 0
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "O":
            coordsum += 100 * y + x

print(coordsum)
