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


def borders(region: list[tuple[int, int]]) -> dict[vec2, list[vec2]]:
    borders: defaultdict[vec2, list[vec2]] = defaultdict(list)
    for point in region:
        point = vec2(*point)
        for d in vec2.cardinal_directions():
            nb = point + d
            if (nb.x, nb.y) not in region:
                borders[d].append(point)
    return borders


border_check_directions = {
    vec2(+1, 0): (vec2(0, -1), vec2(0, +1)),
    vec2(-1, 0): (vec2(0, -1), vec2(0, +1)),
    vec2(0, +1): (vec2(-1, 0), vec2(+1, 0)),
    vec2(0, -1): (vec2(-1, 0), vec2(+1, 0)),
}

border_sort_keys = {
    vec2(+1, 0): lambda v: v.y,
    vec2(-1, 0): lambda v: v.y,
    vec2(0, +1): lambda v: v.x,
    vec2(0, -1): lambda v: v.x,
}


def merge_borders(borders: dict[vec2, list[vec2]]):
    merged_borders: defaultdict[vec2, list[set[vec2]]] = defaultdict(list)
    for d, border_points in borders.items():
        for border_point in sorted(border_points, key=border_sort_keys[d]):
            for merged in merged_borders[d]:
                if any(border_point + offset in merged for offset in border_check_directions[d]):
                    merged.add(border_point)
                    break
            else:
                merged_borders[d].append({border_point})
    return merged_borders


price = 0
for crop, regions in crops_regions.items():
    for region in regions:
        mb = merge_borders(borders(region))
        sides = sum(len(x) for x in mb.values())
        if sides > 100:
            print(f"{crop=} {sides=} {region[0]=}")
        # print(f"A region of {crop} plants with price {len(region)} * {sides} = {len(region) * sides}.")
        price += len(region) * sides

print(price)
