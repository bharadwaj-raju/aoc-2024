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
def move_towards_safe(src: str, dst: str, keymap_name: Literal["NUMPAD", "DPAD"]) -> list[vec2]:
    # never move onto a gap!
    if src == dst:
        return []
    keymap = NUMPAD if keymap_name == "NUMPAD" else DPAD
    src_pos = keymap[src]
    dst_pos = keymap[dst]
    neighbors = src_pos.cardinal_neighbors()

    def score(k: str) -> int:
        return keymap[k].manhattan(src_pos) + keymap[k].manhattan(dst_pos)

    def valid(k: str) -> bool:
        return k != "X" and k != src and keymap[k] in neighbors

    next = min(filter(valid, keymap), key=score)
    return [keymap[next] - keymap[src], *move_towards_safe(next, dst, keymap_name)]


@cache
def move_sequence(keyseq: Iterable[str], keymap_name: Literal["NUMPAD", "DPAD"]) -> list[str]:
    moveseq = []
    curr = "A"
    for key in keyseq:
        moveseq.extend(dir2sym[v] for v in move_towards_safe(curr, key, keymap_name))
        moveseq.append("A")
        curr = key
    return moveseq


def gen_variants(moveseq: Iterable[str]) -> Generator[str]:
    moveseq = "".join(moveseq)
    for variant in product(*(permutations(part) for part in moveseq.split("A"))):
        yield "A".join("".join(part) for part in variant)


def is_safe(moveseq: Iterable[str]) -> bool:
    return True


def your_moves(code: str) -> int:
    return len(
        min(
            map(
                lambda variant: move_sequence(variant, "DPAD"),
                chain(*(gen_variants(move_sequence(v, "DPAD")) for v in gen_variants(move_sequence(code, "NUMPAD")))),
            ),
            key=len,
        )
    )


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
