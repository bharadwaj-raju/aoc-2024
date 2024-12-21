from collections.abc import Generator, Iterable
from functools import cache
from itertools import chain, permutations, product
from typing import Literal
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


@cache
def move_towards_safe(src: str, dst: str, keymap_name: Literal["NUMPAD", "DPAD"]) -> list[list[vec2]]:
    # never move onto a gap!
    keymap = NUMPAD if keymap_name == "NUMPAD" else DPAD
    src_pos = keymap[src]
    dst_pos = keymap[dst]
    neighbors = src_pos.cardinal_neighbors()
    if src == dst:
        return [[]]

    def score(k: str) -> int:
        return keymap[k].manhattan(src_pos) + keymap[k].manhattan(dst_pos)

    def valid(k: str) -> bool:
        return k != "X" and k != src and keymap[k] in neighbors

    lowest_score = min(map(score, filter(valid, keymap)))
    lowest_nexts = [k for k in keymap if valid(k) and score(k) == lowest_score]
    valid_moves = [
        [keymap[eq] - src_pos, *further] for eq in lowest_nexts for further in move_towards_safe(eq, dst, keymap_name)
    ]
    return valid_moves


@cache
def move_sequence(keyseq: Iterable[str], keymap_name: Literal["NUMPAD", "DPAD"]) -> list[list[str]]:
    moveseqs: list[list[list[str]]] = []
    curr = "A"
    for key in keyseq:
        variants = move_towards_safe(curr, key, keymap_name)
        moveseqs.append([[dir2sym[move] for move in variant] + ["A"] for variant in variants])
        curr = key
    return [list(chain(*x)) for x in product(*moveseqs)]


def your_moves(code: str) -> int:
    lowest = None
    for numpad_variant in move_sequence(code, "NUMPAD"):
        for dpad1_variant in move_sequence("".join(numpad_variant), "DPAD"):
            for dpad2_variant in move_sequence("".join(dpad1_variant), "DPAD"):
                if lowest is None or len(dpad2_variant) < lowest:
                    lowest = len(dpad2_variant)
    assert lowest is not None
    return lowest


def complexity(code: str) -> int:
    numeric = int("".join(x for x in code if x in "0123456789"))
    moveseq = your_moves(code)
    print(f"{moveseq} * {numeric}")
    return numeric * moveseq


complexity_sum = 0
for code in codes:
    c = complexity(code)
    print(c)
    complexity_sum += c

print(complexity_sum)
