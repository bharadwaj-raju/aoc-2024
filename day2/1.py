from itertools import pairwise

from util import readlines, sgn

reports = [[int(x) for x in line.split()] for line in readlines()]


def is_safe(report) -> bool:
    direction = sgn(report[1] - report[0])
    for lvl, nxt in pairwise(report):
        if sgn(nxt - lvl) != direction:
            return False
        if not (1 <= abs(nxt - lvl) <= 3):
            return False
    return True


print(sum(is_safe(report) for report in reports))
