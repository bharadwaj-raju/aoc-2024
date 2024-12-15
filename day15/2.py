import os
import time
from util import readtext, grid_get, vec2

grid, movements = readtext().split("\n\n")

widen = {
    "#": "##",
    "O": "[]",
    ".": "..",
    "@": "@.",
}
if "[" in grid:
    grid = [list(row) for row in grid.splitlines()]
else:
    grid = [list("".join(widen[cell] for cell in row)) for row in grid.splitlines()]

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


def normalize_box(grid: Grid, box: vec2) -> vec2:
    at = grid_get(grid, box, default="#")
    if at == "]":
        box = box + vec2(-1, 0)
    return box


def can_push(grid: Grid, box: vec2, dir: vec2) -> bool:
    box = normalize_box(grid, box)
    at = grid_get(grid, box, default="#")
    if at == "#":
        return False
    if at == ".":
        return True
    left = box
    right = box + vec2(+1, 0)
    if dir == vec2(+1, 0):
        return can_push(grid, right + dir, dir)
    elif dir == vec2(-1, 0):
        return can_push(grid, left + dir, dir)
    else:
        return can_push(grid, right + dir, dir) and can_push(grid, left + dir, dir)


def push(grid: Grid, box: vec2, dir: vec2):
    box = normalize_box(grid, box)
    at = grid_get(grid, box, default="#")
    if at in "#.":
        return
    left = box
    right = box + vec2(+1, 0)
    if dir == vec2(+1, 0):
        push(grid, right + dir, dir)
    elif dir == vec2(-1, 0):
        push(grid, left + dir, dir)
    else:
        push(grid, right + dir, dir)
        push(grid, left + dir, dir)
    grid[left.y][left.x] = "."
    grid[right.y][right.x] = "."
    grid[(left + dir).y][(left + dir).x] = "["
    grid[(right + dir).y][(right + dir).x] = "]"


def box_gps(grid: Grid, box: vec2) -> int:
    box = normalize_box(grid, box)
    return (100 * box.y) + box.x


def display(grid: Grid, robot: vec2):
    os.system("clear")
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if vec2(x, y) == robot:
                cell = "@"
            print(cell, end="")
        print()
    print()


for i, move in enumerate(movements):
    # display(grid, robot)
    # print(i, move)
    # time.sleep(0.5)
    in_front = grid_get(grid, robot + move, default="#")
    if in_front == ".":
        robot += move
    elif in_front in "[]":
        if can_push(grid, robot + move, move):
            push(grid, robot + move, move)
            robot += move
    else:
        pass

# display(grid, robot)

coordsum = 0
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "[":
            b = box_gps(grid, vec2(x, y))
            coordsum += b

print(coordsum)
