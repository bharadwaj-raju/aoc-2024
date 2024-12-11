from itertools import chain
from math import floor, log10
from functools import cache

from util import readtext

stones = [int(x) for x in readtext().split()]

print(stones)


def transform(x: int) -> tuple[int] | tuple[int, int]:
    if x == 0:
        return (1,)
    digits = floor(log10(x)) + 1
    if digits % 2 == 0:
        pow10 = 10 ** (digits // 2)
        return (x // pow10, x % pow10)
    return (x * 2024,)


@cache
def stone_project(x: int, n: int) -> int:
    if n == 0:
        return 1
    subset = [x]
    next_subset = chain.from_iterable(transform(x) for x in subset)
    return sum(stone_project(x, n - 1) for x in next_subset)


print(sum(stone_project(x, 25) for x in stones))
