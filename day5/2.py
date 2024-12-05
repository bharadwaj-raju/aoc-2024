from util import readlines


def topologically_valid(
    E: set[tuple[int, int]], ordering: list[int]
) -> tuple[bool, tuple[int, int] | None]:
    indices = {n: i for i, n in enumerate(ordering)}
    subE = {(u, v) for u, v in E if u in indices and v in indices}
    for u, v in subE:
        if not indices[u] < indices[v]:
            return (False, (indices[u], indices[v]))
    return (True, None)


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
    if not topologically_valid(E, ordering)[0]:
        valid = False
        while not valid:
            valid, wrong = topologically_valid(E, ordering)
            if valid:
                break
            assert wrong is not None
            u, v = wrong
            ordering[u], ordering[v] = ordering[v], ordering[u]
        mid = ordering[len(ordering) // 2]
        midsummer += mid

print(midsummer)
