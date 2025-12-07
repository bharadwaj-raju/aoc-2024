from collections.abc import Generator, Iterable
from functools import cache
from itertools import batched, chain, groupby, pairwise, permutations, product
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
def move_towards_safe(
    src: str, dst: str, keymap_name: Literal["NUMPAD", "DPAD"], prev_dirn: vec2 | None = None
) -> list[list[vec2]]:
    # never move onto a gap!
    keymap = NUMPAD if keymap_name == "NUMPAD" else DPAD
    src_pos = keymap[src]
    dst_pos = keymap[dst]
    neighbors = src_pos.cardinal_neighbors()
    if src == dst:
        return [[]]

    def score(k: str) -> int:
        # if the previous direction is the same as the direction to go to for this key
        # that means a huge saving in keypresses later down the line
        return keymap[k].manhattan(src_pos) + keymap[k].manhattan(dst_pos) - (prev_dirn == keymap[k] - src_pos)

    def valid(k: str) -> bool:
        return k != "X" and k != src and keymap[k] in neighbors

    lowest_score = min(map(score, filter(valid, keymap)))
    lowest_nexts = [k for k in keymap if valid(k) and score(k) == lowest_score]
    valid_moves = [
        [keymap[eq] - src_pos, *further]
        for eq in lowest_nexts
        for further in move_towards_safe(eq, dst, keymap_name, prev_dirn=(keymap[eq] - src_pos))
    ]
    return valid_moves


@cache
def move_sequence(keyseq: Iterable[str], keymap_name: Literal["NUMPAD", "DPAD"]) -> list[str]:
    moveseqs: list[list[list[str]]] = []
    curr = "A"
    for key in keyseq:
        variants = move_towards_safe(curr, key, keymap_name)
        moveseqs.append([[dir2sym[move] for move in variant] + ["A"] for variant in variants])
        curr = key
    variants = ["".join(s) for s in [list(chain(*x)) for x in product(*moveseqs)]]
    # lowest_score = min(map(sequence_score, variants))
    return variants
    return [x for x in variants if sequence_score(x) == lowest_score]


@cache
def split_by_A(keyseq: str) -> list[str]:
    # return [s + a for s, a in batched(("".join(it) for _, it in groupby(keyseq, key=lambda c: c != "A")), 2)]
    return [s + "A" for s in keyseq.split("A")]


@cache
def sequence_score(moveseq: str) -> int | tuple[int, int]:
    return len(moveseq) - sum(x == y for x, y in pairwise(moveseq))


@cache
def simulate_2turns(keyseq: str) -> int:
    lowest = float("inf")
    for dpad1_variant in move_sequence(keyseq, "DPAD"):
        for dpad2_variant in move_sequence(dpad1_variant, "DPAD"):
            if lowest is None or len(dpad2_variant) < lowest:
                lowest = len(dpad2_variant)
    assert isinstance(lowest, int)
    return lowest


@cache
def select_lowest_fullorder(keyseq: str, maxdepth: int) -> str:
    if maxdepth == 1:
        return select_lowest_1storder(keyseq)
    if keyseq.count("A") > 1 and split_by_A(keyseq) != [keyseq]:
        return "".join(select_lowest_fullorder(part, maxdepth) for part in split_by_A(keyseq))
    print(f"{keyseq}, {maxdepth}")
    return select_lowest_1storder(select_lowest_fullorder(keyseq, maxdepth - 1))


@cache
def select_lowest_1storder(keyseq: str) -> str:
    # print(f"select_lowest_2ndorder({keyseq})")
    if keyseq.count("A") > 1 and split_by_A(keyseq) != [keyseq]:
        return "".join(select_lowest_1storder(part) for part in split_by_A(keyseq))
    lowest = ""
    lowest_score = float("inf")
    for dpad1_variant in move_sequence(keyseq, "DPAD"):
        for dpad2_variant in move_sequence(dpad1_variant, "DPAD"):
            if len(dpad2_variant) < lowest_score:
                lowest = dpad1_variant
                lowest_score = len(dpad2_variant)
    return lowest
    # if keyseq.count("A") > 1 and split_by_A(keyseq) != [keyseq]:
    #     return "".join(select_lowest_1storder(part) for part in split_by_A(keyseq))
    # lowest = ""
    # lowest_score = float("inf")
    # for dpad1_variant in move_sequence(keyseq, "DPAD"):
    #     if len(dpad1_variant) < lowest_score:
    #         lowest = dpad1_variant
    #         lowest_score = len(dpad1_variant)
    # return lowest


@cache
def select_lowest_2ndorder(keyseq: str) -> str:
    # raise AssertionError
    # print(f"select_lowest_2ndorder({keyseq})")
    if keyseq.count("A") > 1 and split_by_A(keyseq) != [keyseq]:
        return "".join(select_lowest_2ndorder(part) for part in split_by_A(keyseq))
    lowest = ""
    lowest_score = float("inf")
    for dpad1_variant in move_sequence(keyseq, "DPAD"):
        for dpad2_variant in move_sequence(dpad1_variant, "DPAD"):
            if len(dpad2_variant) < lowest_score:
                lowest = dpad2_variant
                lowest_score = len(dpad2_variant)
    return lowest


@cache
def how_many_steps_for(keyseq: str, maxdepth: int) -> int:
    if keyseq.count("A") > 1 and split_by_A(keyseq) != [keyseq]:
        return sum(how_many_steps_for(part, maxdepth) for part in split_by_A(keyseq))
    next_step = select_lowest_fullorder(keyseq, maxdepth)
    if maxdepth == 1:
        return len(next_step)
    return how_many_steps_for(next_step, maxdepth - 1)

    if maxdepth == 2:
        s = select_lowest_1storder(keyseq)
        return len((s))
    # if maxdepth == 2:
    #     return len((select_lowest_2ndorder(keyseq)))
    parts = split_by_A(keyseq)
    return sum(how_many_steps_for(part, maxdepth - 1) for part in parts)


def your_moves_2(code: str, maxdepth: int) -> int:
    total_len = 0
    code = "A" + code
    for src, dst in pairwise(code):
        lowest = float("inf")
        for numpad_variant in move_towards_safe(src, dst, "NUMPAD"):
            s = [dir2sym[move] for move in numpad_variant]
            s = "".join(s)
            lowest = min(lowest, how_many_steps_for(s, maxdepth))
            # depth = 0
            # while depth < maxdepth:
            #     print(f"{depth = }, {len(s) = }", end="\r")
            #     sublen = 0
            #     s = select_lowest_1storder(s)
            #     depth += 1
            # print()
            # if len(s) < lowest:
            #     lowest = len(s)
        assert isinstance(lowest, int)
        total_len += lowest
        # print("\n\n")
    return total_len
    # lowest = float("inf")
    # for numpad_variant in move_sequence(code, "NUMPAD"):
    #     s = numpad_variant
    #     depth = 0
    #     while depth != maxdepth:
    #         print(f"{depth = }, {len(s) = }", end="\r")
    #         s = select_lowest_2ndorder(s)
    #         depth += 2
    #     print()
    #     if len(s) < lowest:
    #         lowest = len(s)
    # assert isinstance(lowest, int)
    # return lowest


def your_moves(code: str, maxdepth: int) -> int:
    lowest = float("inf")

    for numpad_variant in move_sequence(code, "NUMPAD"):
        # variants: list[list[str]] = [numpad_variant]
        #     depth = 0
        #     while depth != 2:
        #         new_variants = []
        #         for variant in variants:
        #             variant = "".join(variant)
        #             split_parts = variant.split("A")
        #             part_sequences: list[list[str]] = []
        #             for part in split_parts:
        #                 part_sequences.extend(move_sequence(part, "DPAD"))
        #                 part_sequences.extend(move_sequence(part[:-1] + "A", "DPAD"))

        #         variants = list(chain(*(move_sequence("".join(variant), "DPAD") for variant in variants)))
        #         depth += 1

        #     lowest = min(lowest, min(map(len, variants)))
        for dpad1_variant in move_sequence("".join(numpad_variant), "DPAD"):
            sim2_lo = ""  # min(move_sequence("".join(dpad1_variant), "DPAD"), key=simulate_2turns)
            print("SIM2", sim2_lo)
            for dpad2_variant in move_sequence("".join(dpad1_variant), "DPAD"):
                if lowest is None or len(dpad2_variant) < lowest:
                    print("LOWEST FOUND", dpad1_variant, dpad1_variant == sim2_lo)
                    lowest = len(dpad2_variant)
    assert isinstance(lowest, int)
    return lowest


def complexity(code: str) -> int:
    numeric = int("".join(x for x in code if x in "0123456789"))
    moveseq = your_moves_2(code, 2)
    print(f"{moveseq} * {numeric}")
    return numeric * moveseq


complexity_sum = 0
for code in codes:
    c = complexity(code)
    print(c)
    complexity_sum += c

print(complexity_sum)
print(select_lowest_2ndorder.cache_info())
