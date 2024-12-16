from collections import defaultdict
from functools import cache
from itertools import chain
from heapq import heapify, heappop, heappush

from util import readgrid, vec2, grid_get, display_grid


def cost(current: vec2, next: vec2, facing: vec2) -> int:
    if next - current == facing:
        return current.manhattan(next)
    return 1000 + current.manhattan(next)


@cache
def path_cost(path: tuple[vec2], initial_facing: vec2) -> int:
    so_far = 0
    curr = path[0]
    facing = initial_facing
    for next in path[1:]:
        so_far += cost(curr, next, facing)
        facing = next - curr
        curr = next
    return so_far


def a_star(grid: list[list[str]], start: vec2, end: vec2, initial_facing: vec2) -> tuple[int, dict[vec2, vec2 | None]]:
    def heuristic(goal: vec2, next: vec2) -> int:
        return next.manhattan(goal)

    def cost(current: vec2, next: vec2, facing: vec2) -> int:
        if next - current == facing:
            return current.manhattan(next)
        return 1000 + current.manhattan(next)

    frontier = [(0, start, initial_facing)]
    heapify(frontier)
    came_from: dict[vec2, vec2 | None] = {}
    cost_so_far: dict[vec2, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current, facing = heappop(frontier)[1:]
        if current == end:
            break
        for next in current.cardinal_neighbors():
            if grid_get(grid, next, default="#") == "#":
                continue
            new_cost = cost_so_far[current] + cost(current, next, facing)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                new_facing = next - current
                heappush(frontier, (priority, next, new_facing))
                came_from[next] = current
    return (cost_so_far[end], came_from)


def a_star_star(
    grid: list[list[str]], start: vec2, end: vec2, initial_facing: vec2, cost_limit: int
) -> list[tuple[vec2, ...]]:
    frontier = [(0, start, initial_facing, [start])]
    heapify(frontier)
    cost_so_far: defaultdict[tuple[vec2, vec2], int | float] = defaultdict(lambda: float("inf"))
    cost_so_far[(start, initial_facing)] = 0
    paths: defaultdict[tuple[vec2, vec2], list[tuple[vec2, ...]]] = defaultdict(list)
    paths[(start, initial_facing)].append((start,))

    while frontier:
        # print(f"remaining: {len(frontier)}", end="\r")
        current_dist, current, facing, path = heappop(frontier)
        for next in current.cardinal_neighbors():
            if grid_get(grid, next, default="#") == "#":
                continue
            new_cost = current_dist + cost(current, next, facing)
            known_cost = float("inf")
            if paths[(next, facing)]:
                known_cost = cost_so_far[(next, facing)]
            if new_cost < known_cost:
                paths[(next, facing)] = [(*path, next)]
                cost_so_far[((next, facing))] = new_cost
                priority = new_cost
                new_facing = next - current
                if new_cost <= cost_limit:
                    heappush(frontier, (priority, next, new_facing, path + [next]))
            elif new_cost == known_cost:
                if new_cost <= cost_limit:
                    paths[(next, facing)].append((*path, next))
                    heappush(frontier, (new_cost, next, next - current, path + [next]))
    # print()
    all_facings = vec2.cardinal_directions()
    return list(chain(*(paths[(end, f)] for f in all_facings)))


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

facing = vec2(+1, 0)  # east

lowest_cost, _ = a_star(grid, start, end, facing)
end_paths = a_star_star(grid, start, end, facing, lowest_cost)

# display_grid(grid, [start, end], list(chain(*all_paths)))

best_seats = set()

for p in end_paths:
    best_seats.update(p)

print(len(best_seats))
