from collections import defaultdict
from functools import cache
from util import readgroups

available_raw, desired = readgroups()
available = sorted(available_raw[0].split(", "), key=len, reverse=True)
available_lengths = set(map(len, available))
available_by_char: defaultdict[str, list[str]] = defaultdict(list)
for avail in available:
    available_by_char[avail[0]].append(avail)


@cache
def match_design(design: str) -> int:
    if not design:
        return 1
    first = design[0]
    possibilities = 0
    for avail in available_by_char[first]:
        if design.startswith(avail):
            possibilities += match_design(design[len(avail) :])
    return possibilities


print(sum(map(match_design, desired)))
