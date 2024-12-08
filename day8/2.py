from util import grid_get, readgrid, vec2

from itertools import combinations
from collections import defaultdict
from string import ascii_letters, digits

same_freqs: defaultdict[str, set[vec2]] = defaultdict(set)

grid = readgrid()

for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell in ascii_letters + digits:
            same_freqs[cell].add(vec2(x, y))

antinodes = set()

for freq, antennae in same_freqs.items():
    for a, b in combinations(antennae, r=2):
        for start, dirn in ((a, (a - b)), (b, (b - a))):
            curr = start
            while grid_get(grid, curr, "~") != "~":
                antinodes.add(curr)
                curr += dirn

print(len(antinodes))
