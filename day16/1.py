from heapq import heapify, heappop, heappush
from util import readgrid, vec2, grid_get


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
                came_from[next] = current
    return (cost_so_far[end], came_from)


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

cost, came_from = a_star(grid, start, end, facing)

path = []
curr = end
while curr != start:
    path.append(curr)
    curr = came_from[curr]
    assert curr is not None
path.reverse()
print(path)

print(cost)
