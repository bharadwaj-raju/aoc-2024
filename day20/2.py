from dataclasses import dataclass, field
from heapq import heapify, heappop, heappush
from functools import cache

from util import grid_get, readgrid, vec2

grid = readgrid()

start = None
end = None
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == "S":
            start = vec2(x, y)
        elif cell == "E":
            end = vec2(x, y)

assert start is not None
assert end is not None


def a_star(grid: list[list[str]], start: vec2, end: vec2) -> tuple[int, dict[vec2, vec2 | None]]:
    @dataclass(frozen=True, order=True)
    class Item:
        priority: int
        point: vec2 = field(compare=False)

    @cache
    def heuristic(next: vec2) -> int:
        return next.manhattan(end)

    frontier = [Item(0, start)]
    heapify(frontier)
    came_from: dict[vec2, vec2 | None] = {}
    cost_so_far: dict[vec2, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heappop(frontier).point
        if current == end:
            break
        for next in current.cardinal_neighbors():
            if grid_get(grid, next, default="#") == "#":
                continue
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next)
                heappush(frontier, Item(priority, next))
                came_from[next] = current
    return (cost_so_far[end], came_from)


def construct_path(came_from: dict[vec2, vec2 | None], start: vec2, end: vec2) -> list[vec2]:
    path = [end]
    while path[-1] != start:
        prev = came_from[path[-1]]
        assert prev
        path.append(prev)
    path.reverse()
    return path


normal_time, normal_came_from = a_star(grid, start, end)
normal_path = construct_path(normal_came_from, start, end)

normal_path_indices = {point: i for i, point in enumerate(normal_path)}

MAX_CHEAT_LEN = 20

AT_LEAST = 100

at_least = 0
for start_time, cheat_start in enumerate(normal_path):
    if start_time > len(normal_path) - AT_LEAST:
        break
    for cheat_end in normal_path[start_time + AT_LEAST :]:
        cheat_dist = cheat_start.manhattan(cheat_end)
        normal_end_time = normal_path_indices[cheat_end]
        cheat_end_time = start_time + cheat_dist
        if cheat_dist <= MAX_CHEAT_LEN and (normal_end_time - cheat_end_time) >= AT_LEAST:
            at_least += 1

print(f"{at_least} cheats would save at least {AT_LEAST} picoseconds.")
