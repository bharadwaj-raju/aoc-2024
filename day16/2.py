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
    return so_far + 1


def all_paths(grid: list[list[str]], start: vec2, end: vec2, path=None) -> list[list[vec2]]:
    from_here = []
    if path is None:
        path = [start]
    # print(f"all_paths({start=})")
    for next in start.cardinal_neighbors():
        if next == end:
            from_here.append([next, end])
        if next in path or grid_get(grid, next, default="#") == "#":
            continue
        # print(f"\t{next}")
        if True or next != end:
            try:
                for branch in all_paths(grid, next, end, path + [next]):
                    from_here.append([next, *branch])
            except RecursionError:
                pass
    return from_here


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


def display(grid: list[list[str]], highlight: Iterable[vec2]):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if vec2(x, y) in highlight:
                print("O", end="")
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
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                new_facing = next - current
                heappush(frontier, (priority, next, new_facing))
                came_from[next].add(current)
    return (cost_so_far[end], came_from)


lowest_cost, came_from = a_star(grid, start, end, facing)

for c in came_from.values():
    if len(c) > 1:
        display(grid, c)

ap = all_paths(grid, start, end)

best_seats = set()

for path in ap:
    grid_c = [row.copy() for row in grid]
    if path[-1] != end:
        continue
    pc = path_cost(path, initial_facing=facing)
    if pc > 13000:
        continue
    if pc == lowest_cost + 1000:
        print("ayyyyyyyy")
        best_seats.update(path)
    for el in path:
        grid_c[el.y][el.x] = "O"
    print("\n".join("".join(row) for row in grid_c))
    print(pc)

print("ANS", len(best_seats) + 1)

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
