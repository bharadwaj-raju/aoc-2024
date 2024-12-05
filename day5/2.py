from util import readlines


def outgoing(E: set[tuple[int, int]], source: int) -> set[int]:
    return {dst for src, dst in E if src == source}


def incoming(E: set[tuple[int, int]], destination: int) -> set[int]:
    return {src for src, dst in E if dst == destination}


# Kahn's algorithm
def toposort(V: set[int], E: set[tuple[int, int]]) -> list[int]:
    order = []
    independent = {v for v in V if not incoming(E, v)}
    while independent:
        n = independent.pop()
        order.append(n)
        for m in outgoing(E, n):
            E.remove((n, m))
            if not incoming(E, m):
                independent.add(m)

    return order


def topologically_valid(E: set[tuple[int, int]], ordering: list[int]) -> bool:
    indices = {n: i for i, n in enumerate(ordering)}
    subE = {(u, v) for u, v in E if u in indices and v in indices}
    return all(indices[u] < indices[v] for u, v in subE)


E: set[tuple[int, int]] = set()
orderings: list[list[int]] = []
for line in readlines():
    if not line:
        continue
    if "|" in line:
        u, v = [int(x.strip()) for x in line.split("|")]
        E.add((u, v))
    else:
        orderings.append([int(x) for x in line.split(",")])


midsummer = 0

for ordering in orderings:
    if not topologically_valid(E, ordering):
        V = set(ordering)
        subE = {(u, v) for u, v in E if u in V and v in V}
        ordering = toposort(V, subE)
        mid = ordering[len(ordering) // 2]
        midsummer += mid

print(midsummer)
