from itertools import pairwise
from typing import Literal

from util import readlines, sgn

reports = [[int(x) for x in line.split()] for line in readlines()]


def is_safe(report) -> tuple[bool, int, Literal["direction", "magnitude", ""]]:
    direction = sgn(report[1] - report[0])
    for i, (lvl, nxt) in enumerate(pairwise(report)):
        if sgn(nxt - lvl) != direction:
            return (False, i, "direction")
        if not (1 <= abs(nxt - lvl) <= 3):
            return (False, i, "magnitude")
    return (True, len(report), "")


safe_count = 0
for report in reports:
    safe, last_pair, reason = is_safe(report)
    if not safe:
        if reason == "direction" and is_safe(report[1:])[0]:
            safe = True
        else:
            report_dampened_left = report[:last_pair] + report[last_pair + 1 :]
            report_dampened_right = report[: last_pair + 1] + report[last_pair + 2 :]
            safe = is_safe(report_dampened_left)[0] or is_safe(report_dampened_right)[0]

    if safe:
        safe_count += 1

print(safe_count)
