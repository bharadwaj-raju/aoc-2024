from collections.abc import Iterable
from heapq import heapify, heappop, heappush
from util import vec2, readlines

corrupted = [vec2(*map(int, p.split(","))) for p in readlines()]

if len(corrupted) < 100:
    # smallinput
    bounds = (6, 6)
else:
    bounds = (70, 70)


def reachable(obstacles: Iterable[vec2], bounds: tuple[int, int], start: vec2, end: vec2) -> bool:
    obstacles = set(obstacles)
    frontier = [(0, start)]
    heapify(frontier)
    came_from: dict[vec2, vec2 | None] = {}
    cost_so_far: dict[vec2, int] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heappop(frontier)[1]
        if current == end:
            return True
        for next in current.cardinal_neighbors():
            if next in obstacles:
                continue
            if next.x < 0 or next.x > bounds[0] or next.y < 0 or next.y > bounds[1]:
                continue
            new_cost = cost_so_far[current] + current.manhattan(next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                heappush(frontier, (priority, next))
                came_from[next] = current
    return False


low, high = 0, len(corrupted)

steps = 0
while low != high:
    steps += 1
    mid = (low + high) // 2
    if reachable(corrupted[:mid], bounds, vec2(0, 0), vec2(*bounds)):
        low = mid + 1
    else:
        high = mid

print(f"First byte that blocks is #{low-1}, found in {steps} steps")
print(corrupted[low - 1])
