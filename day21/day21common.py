from collections.abc import Iterable
from functools import cache
from itertools import chain, pairwise, product
from typing import Literal

from util import vec2

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


dir2sym = {
    vec2(+0, -1): "^",
    vec2(+1, +0): ">",
    vec2(+0, +1): "v",
    vec2(-1, +0): "<",
}

# Can we get the correct shortest sequence "by construction" as it were?
# There are only so many sequences of moves (on a dpad) that can occur before
# we reset to A.
# The solution to any sequence can be split into independent subproblems on As.
#
# So, how about we have a "learning phase"?
# We will generate all ways to create a particular dpad move on the next level.
# "If I want some Z key pressed here, what are all the ways the next level can move?"
# We will simulate it all to some number of steps, and keep track of which is the
# most efficient way to achieve any particular keypress.
#
# Once we have that, finding the most efficient next level move sequence for a given
# move sequence is just a matter of mapping each key on this level to the calculated
# most-efficient move.

best_moves: dict[tuple[str, str], str] = {
    ("A", "^"): "<",
    ("A", ">"): "v",
    ("A", "v"): "<v",
    ("A", "<"): "v<<",
    ("^", "A"): ">",
    (">", "A"): "^",
    ("v", "A"): "^>",
    ("<", "A"): ">>^",
    ("v", ">"): ">",
    ("v", "<"): "<",
    ("v", "^"): "^",
    ("<", "v"): ">",
    ("<", ">"): ">>",
    ("<", "^"): ">^",
    ("^", "<"): "v<",
    ("^", "v"): "v",
    ("^", ">"): "v>",
    (">", "<"): "<<",
    (">", "v"): "<",
    (">", "^"): "<^",
}


# We are definitely on a good track here.
# We just need to extend basic_best_moves (which only gives you best moves from A)
# to be something generalized that gives you the best move from anywhere
# for multi-non-A sequences like `>>^`
# note! the maximum valid (safe + pruning obv inefficiencies) multi-non-A sequence
# length for a dpad move is 3
# for numpad moves it is higher, like 5
# but we can definitely simulate all that!!


def construct_best_move(seq: str) -> str:
    out = []
    for i, c in enumerate(seq):
        p = seq[i - 1] if i != 0 else "A"
        if c == p:
            out.append("A")  # just hit Accept again to enter the same char
        else:
            out.append(best_moves[p, c] + "A")
    # print(out)
    return "".join(out)


def split_by_A(keyseq: str) -> list[str]:
    split = []
    accum = []
    for c in keyseq:
        if c == "A":
            split.append("".join(accum) + "A")
            accum.clear()
        else:
            accum.append(c)
    if accum:
        split.append("".join(accum))
    return split
    # return [s + a for s, a in batched(("".join(it) for _, it in groupby(keyseq, key=lambda c: c != "A")), 2)]
    # return [s + "A" for s in keyseq.split("A")]


# So, just constructing the move sequence up to 25 layers is still very slow, and takes too much memory.
# Instead, remember that we just need the length of the sequence. We can take advantage of the fact that
# splitting across A creates independent subproblems, and we can just find, with memoization, the length after N
# steps of these subproblems. The cache avoids a lot of repeated work, and this performs very well.


@cache
def best_move_len(seq: str, n: int) -> int:
    if n == 0:
        return len(seq)
    if seq.count("A") > 1:
        return sum(best_move_len(subseq, n) for subseq in split_by_A(seq))
    seq = construct_best_move(seq)
    if n == 1:
        return len(seq)
    return best_move_len(seq, n - 1)


def move_towards_safe(
    src: str,
    dst: str,
    keymap_name: Literal["NUMPAD", "DPAD"],
    prev_dirn: vec2 | None = None,
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
        return (
            keymap[k].manhattan(src_pos)
            + keymap[k].manhattan(dst_pos)
            - (prev_dirn == keymap[k] - src_pos)
        )

    def valid(k: str) -> bool:
        return k != "X" and k != src and keymap[k] in neighbors

    lowest_score = min(map(score, filter(valid, keymap)))
    lowest_nexts = [k for k in keymap if valid(k) and score(k) == lowest_score]
    valid_moves = [
        [keymap[eq] - src_pos, *further]
        for eq in lowest_nexts
        for further in move_towards_safe(
            eq, dst, keymap_name, prev_dirn=(keymap[eq] - src_pos)
        )
    ]
    return valid_moves


@cache
def sequence_score(moveseq: str) -> int:
    return len(moveseq) - sum(x == y for x, y in pairwise(moveseq))


@cache
def move_sequence(
    keyseq: Iterable[str], keymap_name: Literal["NUMPAD", "DPAD"]
) -> list[str]:
    moveseqs: list[list[list[str]]] = []
    # if
    curr = "A"
    for key in keyseq:
        variants = move_towards_safe(curr, key, keymap_name)
        moveseqs.append(
            [[dir2sym[move] for move in variant] + ["A"] for variant in variants]
        )
        curr = key
    variants = ["".join(s) for s in [list(chain(*x)) for x in product(*moveseqs)]]
    lowest_score = min(map(sequence_score, variants))
    return [x for x in variants if sequence_score(x) == lowest_score]


def extract_numeric_part(code: str) -> int:
    return int("".join(x for x in code if x.isdigit()).lstrip("0"))


def complexity(code: str, layers: int) -> int:
    move_length = min(
        best_move_len(seq, layers) for seq in move_sequence(code, "NUMPAD")
    )
    numeric = extract_numeric_part(code)
    return move_length * numeric
