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
        anti1 = a + (a - b)
        anti2 = b + (b - a)
        for anti in (anti1, anti2):
            if grid_get(grid, anti, "~") != "~":
                antinodes.add(anti)

print(len(antinodes))
