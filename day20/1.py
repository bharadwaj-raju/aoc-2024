from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heapify, heappop, heappush
from functools import cache

from util import readgrid, vec2, grid_get

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


def viable_cheats(grid: list[list[str]], curr: vec2) -> list[tuple[vec2, vec2]]:
    return [
        (curr, end)
        for first in curr.cardinal_neighbors()
        for end in first.cardinal_neighbors()
        if grid_get(grid, end, "#") != "#" and curr != end
    ]


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

cheat_savings: defaultdict[int, set[tuple[vec2, vec2]]] = defaultdict(set)

for cost_so_far, point in enumerate(normal_path):
    for cheat in viable_cheats(grid, point):
        _, cheat_end = cheat
        try:
            jump_to = normal_path_indices[cheat_end]
            cheat_time = cost_so_far + 2 + (normal_time - jump_to)
            if cheat_time < normal_time:
                cheat_savings[normal_time - cheat_time].add(cheat)
        except KeyError:
            pass

at_least_100 = 0
for savings in sorted(cheat_savings.keys()):
    # print(f"There are {len(cheat_savings[savings])} cheats that save {savings} picoseconds.")
    if savings >= 100:
        at_least_100 += len(cheat_savings[savings])

print(f"{at_least_100} cheats would save at least 100 picoseconds.")
