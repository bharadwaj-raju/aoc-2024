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
def match_design(design: str) -> bool:
    if not design:
        return True
    first = design[0]
    for avail in available_by_char[first]:
        if design.startswith(avail) and match_design(design[len(avail) :]):
            return True
    return False


print(sum(map(match_design, desired)))
