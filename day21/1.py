from collections.abc import Iterable
from functools import cache
from util import readlines, vec2

codes = readlines()

print(codes)

NUMPAD = {
    "A": vec2(0, 0),
    "0": vec2(-1, 0),
    "3": vec2(0, -1),
    "6": vec2(0, -2),
    "9": vec2(0, -3),
    "2": vec2(-1, -1),
    "5": vec2(-1, -2),
    "8": vec2(-1, -3),
    "1": vec2(-2, -1),
    "4": vec2(-2, -2),
    "7": vec2(-2, -3),
    "X": vec2(-2, 0),
}

DPAD = {
    "A": vec2(0, 0),
    "^": vec2(-1, 0),
    "<": vec2(-2, +1),
    "v": vec2(-1, +1),
    ">": vec2(0, +1),
    "X": vec2(-2, 0),
}


sym2dir = {
    "^": vec2(+0, -1),
    ">": vec2(+1, +0),
    "v": vec2(+0, +1),
    "<": vec2(-1, +0),
}

dir2sym = {
    vec2(+0, -1): "^",
    vec2(+1, +0): ">",
    vec2(+0, +1): "v",
    vec2(-1, +0): "<",
}


def move_towards_safe(src: str, dst: str, keymap: dict[str, vec2]) -> list[vec2]:
    # never move onto a gap!
    if src == dst:
        return []
    next = min(
        filter(lambda k: k != "X" and k != src and keymap[k] in keymap[src].cardinal_neighbors(), keymap),
        key=lambda k: keymap[k].manhattan(keymap[src]) + keymap[k].manhattan(keymap[dst]),
    )
    return [keymap[next] - keymap[src], *move_towards_safe(next, dst, keymap)]


def move_sequence(keyseq: Iterable[str], keymap: dict[str, vec2]) -> list[str]:
    moveseq = []
    curr = "A"
    for key in keyseq:
        moveseq.extend(dir2sym[v] for v in move_towards_safe(curr, key, keymap))
        moveseq.append("A")
        curr = key
    return moveseq


print(("".join((move_sequence(move_sequence(codes[0], NUMPAD), DPAD)))))

print(("".join(move_sequence(move_sequence(move_sequence(codes[0], NUMPAD), DPAD), DPAD))))
print(("".join(move_sequence("v<<A>>^A<A>AvA<^AA>A<vAAA>^A", DPAD))))


def your_moves(code: str) -> list[str]:
    return move_sequence(move_sequence(move_sequence(code, NUMPAD), DPAD), DPAD)


def complexity(code: str) -> int:
    numeric = int("".join(x for x in code if x in "0123456789"))
    moveseq = len(your_moves(code))
    print(f"{numeric} * {moveseq}")
    return numeric * moveseq


complexity_sum = 0
for code in codes:
    c = complexity(code)
    print(c)
    complexity_sum += c

print(complexity_sum)
