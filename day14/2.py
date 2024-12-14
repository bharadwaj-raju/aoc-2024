import time
import os
from pprint import pp

from util import grid_get, vec2, readlines


def parse_line(line: str) -> tuple[vec2, vec2]:
    p, v = line.strip().split()
    p = vec2(*map(int, p.split("=")[-1].split(",")))
    v = vec2(*map(int, v.split("=")[-1].split(",")))
    return p, v


robots = [parse_line(line) for line in readlines()]

BOUNDS = (11, 7) if len(robots) < 30 else (101, 103)


def move(pos: vec2, vel: vec2) -> vec2:
    new_pos = pos + vel
    return vec2(new_pos.x % BOUNDS[0], new_pos.y % BOUNDS[1])


def make_grid(robots: list[vec2]) -> list[str]:
    grid: list[list[str]] = []
    for y in range(BOUNDS[1]):
        row = [" "] * BOUNDS[0]
        grid.append(row)
    for pos in robots:
        grid[pos.y][pos.x] = "#"
    return ["".join(row) for row in grid]


seconds = 0
while True:
    try:
        grid = make_grid([pos for pos, _ in robots])
        found = False
        for row in grid:
            if "############" in row:
                found = True
                break
        if found:
            print("\n" * 124)
            for row in grid:
                print(row)
            print(seconds)
        robots = [(move(pos, vel), vel) for pos, vel in robots]
        seconds += 1
        # time.sleep(0.5)
    except KeyboardInterrupt:
        print("Bye!")
        break
