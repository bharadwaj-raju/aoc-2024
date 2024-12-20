from collections import defaultdict
from heapq import heapify, heappop, heappush
from util import readgrid, vec2, grid_get, display_grid

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


def a_star(
    grid: list[list[str]], start: vec2, end: vec2, cheat: tuple[vec2, vec2] | None = None
) -> tuple[int, dict[vec2, vec2 | None]]:
    def heuristic(next: vec2) -> int:
        return next.manhattan(end)

    frontier = [(0, start)]
    heapify(frontier)
    came_from: dict[vec2, vec2 | None] = {}
    cost_so_far: dict[vec2, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heappop(frontier)[1]
        if current == end:
            break
        if cheat and current == cheat[0]:
            new_cost = cost_so_far[current] + 2
            cost_so_far[cheat[1]] = new_cost
            heappush(frontier, (new_cost, cheat[1]))
        for next in current.cardinal_neighbors():
            if grid_get(grid, next, default="#") == "#":
                continue
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next)
                heappush(frontier, (priority, next))
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

cheat_savings: defaultdict[int, set[tuple[vec2, vec2]]] = defaultdict(set)

for cost_so_far, point in enumerate(normal_path):
    for cheat in viable_cheats(grid, point):
        cheat_start, cheat_end = cheat
        cheat_time, cheat_came_from = a_star(grid, point, end, cheat)
        total_cheat_time = cost_so_far + cheat_time
        if total_cheat_time < normal_time:
            cheat_savings[normal_time - total_cheat_time].add(cheat)

at_least_100 = 0
for savings in sorted(cheat_savings.keys()):
    print(f"There are {len(cheat_savings[savings])} cheats that save {savings} picoseconds.")
    if savings >= 100:
        at_least_100 += len(cheat_savings[savings])

print(f"{at_least_100} cheats would save at least 100 picoseconds.")
