from collections import defaultdict
from itertools import groupby

from util import readgrid, vec2

garden = readgrid()

consumed = set()

crops_regions: defaultdict[str, list[list[tuple[int, int]]]] = defaultdict(list)

for y, row in enumerate(garden):
    for k, g in groupby(enumerate(row), key=lambda item: item[1]):
        g = list(g)
        start, end = g[0][0], g[-1][0]
        for region in crops_regions[k]:
            if any(p[0] in range(start, end + 1) and p[1] == y - 1 for p in region):
                region.extend((x, y) for x in range(start, end + 1))
        crops_regions[k].append([(x, y) for x in range(start, end + 1)])

# merge finally
# useful in the case of
# A XYZ A
# AAAAAAA
# etc.
for crop, regions in crops_regions.items():
    merged_regions = []
    for region in regions:
        s_region = set(region)
        for merged in merged_regions:
            s_merged = set(merged)
            if s_merged & s_region:
                merged.extend(s_region - s_merged)
                break
        else:
            merged_regions.append(region)
    crops_regions[crop] = merged_regions


def perimeter(region: list[tuple[int, int]]) -> int:
    count = 0
    for point in region:
        point = vec2(*point)
        for nb in point.cardinal_neighbors():
            if (nb.x, nb.y) not in region:
                count += 1
    return count


price = 0
for crop, regions in crops_regions.items():
    for region in regions:
        # print(
        #     f"A region of {crop} plants with price {len(region)} * {perimeter(garden, region)} = {len(region) * perimeter(garden, region)}."
        # )
        price += len(region) * perimeter(region)

print(price)
