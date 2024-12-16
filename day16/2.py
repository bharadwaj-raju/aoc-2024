from collections import defaultdict, deque
from collections.abc import Iterable, Sequence
from functools import cache
from itertools import pairwise
from heapq import heapify, heappop, heappush
from util import readgrid, vec2, grid_get


def cost(current: vec2, next: vec2, facing: vec2) -> int:
    if next - current == facing:
        return current.manhattan(next)
    return 1000 + current.manhattan(next)


def path_cost(path: list[vec2], initial_facing: vec2) -> int:
    so_far = 0
    curr = path[0]
    facing = initial_facing
    for next in path[1:]:
        so_far += cost(curr, next, facing)
        facing = next - curr
        curr = next
    return so_far


def all_paths(
    grid: list[list[str]], start: vec2, end: vec2, initial_facing: vec2, cost_limit: int
) -> list[list[vec2]]:
    paths = []

    stack = [(start, [start], set([start]), initial_facing, 0)]  # (current position, current path, visited set)

    while stack:
        print(f"found: {len(paths)} remaining: {len(stack)}", end="\r")
        curr, path, visited, facing, cost_so_far = stack.pop()

        if curr == end:
            paths.append(path)
            continue

        # Explore all four directions
        for nb in curr.cardinal_neighbors():
            if grid_get(grid, nb, "#") == "#":
                continue
            new_cost = cost_so_far + cost(curr, nb, facing)
            if new_cost > cost_limit:
                # print("over limit")
                continue
            if nb not in visited:
                stack.append((nb, path + [nb], visited | {nb}, nb - curr, new_cost))

    return paths


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


def display(grid: list[list[str]], highlight_o: Iterable[vec2], highlight_x: Iterable[vec2]):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if vec2(x, y) in highlight_o:
                print("O", end="")
            elif vec2(x, y) in highlight_x:
                print("X", end="")
            else:
                print(cell, end="")
        print()


def a_star(grid: list[list[str]], start: vec2, end: vec2, initial_facing: vec2) -> tuple[int, dict[vec2, set[vec2]]]:
    def heuristic(goal: vec2, next: vec2) -> int:
        return next.manhattan(goal)

    def cost(current: vec2, next: vec2, facing: vec2) -> int:
        if next - current == facing:
            return current.manhattan(next)
        return 1000 + current.manhattan(next)

    frontier = [(0, start, initial_facing)]
    heapify(frontier)
    came_from: defaultdict[vec2, set[vec2]] = defaultdict(set)
    cost_so_far: dict[vec2, int] = {}
    cost_so_far[start] = 0

    while frontier:
        current, facing = heappop(frontier)[1:]
        # print(current)
        if current == end:
            break
        for next in current.cardinal_neighbors():
            if grid_get(grid, next, default="#") == "#":
                continue
            new_cost = cost_so_far[current] + cost(current, next, facing)
            if next not in cost_so_far or new_cost <= cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost  # + heuristic(end, next)
                new_facing = next - current
                heappush(frontier, (priority, next, new_facing))
                came_from[next].add(current)
    return (cost_so_far[end], came_from)


lowest_cost, came_from = a_star(grid, start, end, facing)


def cf2path(came_from):
    path = []
    curr = {end}
    while curr != {start}:
        path.extend(curr)
        # for c in curr:
        #     print(came_from[c])
        curr = set.union(*[came_from[c] for c in curr])
        if len(curr) > 1:
            print("!!!!!!!!")
    path.reverse()
    return path


# display(grid, cf2path(came_from), [])

# best_seats = set(cf2path(came_from))

# for n, c in came_from.items():
#     if len(c) > 1:
#         print(c)
#         for p in c:
#             grid_c = [row.copy() for row in grid]
#             grid_c[p.y][p.x] = "#"
#             display(grid_c, [], [])
#             try_cost, try_came_from = a_star(grid_c, start, end, facing)
#             if try_cost <= lowest_cost:
#                 best_seats.update(cf2path(try_came_from))


# print(len(best_seats))


import sys

# sys.exit(1)
ap = all_paths(grid, start, end, facing, lowest_cost)


best_seats = set()

for path in ap:
    pc = path_cost(path, initial_facing=facing)
    if pc == lowest_cost:
        best_seats.update(path)

print("ANS", len(best_seats))

# lowest_cost, came_from, costs_so_far = breadth_first(grid, start, end, facing)

# for c in came_from.values():
#     if len(c) > 1:
#         for p in c:
#             grid[p.y][p.x] = "X"


best_seats: set[vec2] = set()
# for path_cost, path in full_search(grid, start, end, facing, 0, lowest_cost, set()):
#     print(path_cost, path)
#     if path[-1] == end and path_cost == lowest_cost:
#         best_seats.update(path)


# def visit(curr: vec2, end: vec2, costs_to, so_far):
#     for nb in curr.cardinal_neighbors():
#         if costs_so_far[nb]


print(len(best_seats))

print(
    path_cost(
        [
            vec2(x=1, y=12),
            vec2(x=1, y=11),
            vec2(x=2, y=11),
            vec2(x=3, y=11),
            vec2(x=4, y=11),
            vec2(x=5, y=11),
            vec2(x=5, y=10),
            vec2(x=5, y=9),
            vec2(x=5, y=8),
            vec2(x=5, y=7),
            vec2(x=6, y=7),
            vec2(x=7, y=7),
            vec2(x=8, y=7),
            vec2(x=9, y=7),
            vec2(x=10, y=7),
            vec2(x=11, y=7),
            vec2(x=11, y=8),
            vec2(x=11, y=9),
            vec2(x=11, y=10),
            vec2(x=11, y=11),
            vec2(x=11, y=12),
            vec2(x=11, y=13),
            vec2(x=12, y=13),
            vec2(x=13, y=13),
            vec2(x=13, y=12),
            vec2(x=13, y=11),
            vec2(x=13, y=10),
            vec2(x=13, y=9),
            vec2(x=13, y=8),
            vec2(x=13, y=7),
            vec2(x=13, y=6),
            vec2(x=13, y=5),
            vec2(x=13, y=4),
            vec2(x=13, y=3),
            vec2(x=13, y=2),
            vec2(x=13, y=1),
        ],
        initial_facing=vec2(+1, 0),
    )
)
