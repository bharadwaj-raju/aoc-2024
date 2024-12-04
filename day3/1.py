from util import readtext

mem = readtext()


def findall(needle: str, haystack: str) -> list[int]:
    posns = []
    for i, _ in enumerate(haystack):
        if haystack[i:].startswith(needle):
            posns.append(i)
    return posns


def trydigit(mem: str, pos: int) -> tuple[int, int]:
    digits = []
    while mem[pos] in "1234567890":
        digits.append(mem[pos])
        pos += 1
    return (int("".join(digits)), pos)


def trymul(mem):
    if not mem.startswith("mul("):
        return 0
    pos = 4
    try:
        num1, pos = trydigit(mem, pos)
        if mem[pos] != ",":
            raise ValueError
        pos += 1
        num2, pos = trydigit(mem, pos)
        if mem[pos] != ")":
            raise ValueError
        pos += 1
        return num1 * num2
    except (IndexError, ValueError):
        return 0


print(sum(trymul(mem[i:]) for i in findall("mul(", mem)))
