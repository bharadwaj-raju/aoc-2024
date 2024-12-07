from collections.abc import Iterable, Sequence
from util import readlines, interleave
from itertools import combinations_with_replacement, batched, product

eqns = []
for line in readlines():
    lhs, rhs = line.split(": ")
    eqns.append((int(lhs), [int(x) for x in rhs.split()]))


def sub_eval(l: int, op: str, r: int) -> int:
    if op == "*":
        return l * r
    elif op == "+":
        return l + r
    raise ValueError


def try_eval(target: int, parts: Iterable[int], ops: Iterable[str]) -> bool:
    expr = list(interleave(parts, ops))
    so_far = sub_eval(*expr[:3])
    if so_far > target:
        return False
    for next_op, next_part in batched(expr[3:], 2):
        so_far = sub_eval(so_far, next_op, next_part)
        if so_far > target:
            return False
    return so_far == target


def solvable(target: int, parts: Sequence[int]) -> bool:
    for ops in product("+*", repeat=len(parts) - 1):
        if try_eval(target, parts, ops):
            return True
    return False


print(sum(target for target, parts in eqns if solvable(target, parts)))
