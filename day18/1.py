from collections.abc import Iterable
from heapq import heapify, heappop, heappush
from util import vec2, readlines

corrupted = [vec2(*map(int, p.split(","))) for p in readlines()]

if len(corrupted) < 100:
    # smallinput
    bounds = (6, 6)
    cutoff = 12
else:
    bounds = (70, 70)
    cutoff = 1024

corrupted = corrupted[:cutoff]


def dijkstra(obstacles: Iterable[vec2], bounds: tuple[int, int], start: vec2, end: vec2) -> int:
    obstacles = set(obstacles)
    frontier = [(0, start)]
    heapify(frontier)
    cost_so_far: dict[vec2, int] = {}
    cost_so_far[start] = 0

    while frontier:
        current = heappop(frontier)[1]
        if current == end:
            break
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
    return cost_so_far[end]


path_length = dijkstra(corrupted, bounds, vec2(0, 0), vec2(*bounds))

print(path_length)
