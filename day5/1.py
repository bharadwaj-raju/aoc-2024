from util import readlines


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
    if topologically_valid(E, ordering):
        # print(f"VALID {ordering}")
        mid = ordering[len(ordering) // 2]
        # print(f"\t{mid=}")
        midsummer += mid

print(midsummer)
