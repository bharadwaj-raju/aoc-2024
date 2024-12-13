from collections.abc import Iterable
from math import inf, lcm

from util import readgroups, vec2


# actually all the equations in our input have only one possible solution
# I just wrote this for verification
def possible_solutions(a: vec2, b: vec2, prize: vec2) -> int | float:
    # xd + ye = f
    # xg + yh = i
    # solutions are only possible if:
    # d/g = e/h = f/i (infinitely many)
    # or
    # d/g != e/h (one)
    # x = presses of A
    # y = presses of B
    # first equation is about X travel, second about Y travel
    if a.x / a.y == b.x / b.y:
        if a.x / a.y == prize.x / prize.y:
            return inf
        return 0
    return 1


def solve_one(a: vec2, b: vec2, prize: vec2) -> tuple[float, float]:
    eq1 = [a.x, b.x, prize.x]
    eq2 = [a.y, b.y, prize.y]
    x_lcm = lcm(a.x, a.y)
    eq1 = [c * x_lcm // a.x for c in eq1]
    eq2 = [c * x_lcm // a.y for c in eq2]
    eq1 = [c - d for c, d in zip(eq1, eq2)]
    y = eq1[2] / eq1[1]
    x = (eq2[2] - y * eq2[1]) / eq2[0]
    return (x, y)


def feasible(x: float, y: float) -> int:
    return x.is_integer() and y.is_integer() and (0 <= x) and (0 <= y)


def tokens(x: int, y: int) -> int:
    return (3 * x) + y


def parse_group(lines: Iterable[str]) -> tuple[vec2, vec2, vec2]:
    def parse_line(line: str) -> vec2:
        dx, dy = line.split(": ")[-1].split(", ")
        dx = int(dx.replace("X+", "").replace("X=", ""))
        dy = int(dy.replace("Y+", "").replace("Y=", ""))
        return vec2(dx, dy)

    a = None
    b = None
    prize = None
    for line in lines:
        if "Button A" in line:
            a = parse_line(line)
        elif "Button B" in line:
            b = parse_line(line)
        else:
            prize = parse_line(line)
            prize = vec2(prize.x + 10000000000000, prize.y + 10000000000000)

    assert a is not None
    assert b is not None
    assert prize is not None

    return (a, b, prize)


machines = [parse_group(group) for group in readgroups()]

tokensum = 0
for m in machines:
    n_sol = possible_solutions(*m)
    if n_sol == 1:
        sol = solve_one(*m)
        if feasible(*sol):
            x, y = map(int, sol)
            tokensum += tokens(x, y)
    else:
        print("oops")
print(tokensum)
