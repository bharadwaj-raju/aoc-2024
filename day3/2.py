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


muls = findall("mul(", mem)
dos = findall("do()", mem)
donts = findall("don't()", mem)

dos.insert(0, 0)
dos.reverse()
donts.reverse()

mulsum = 0

for mulpos in muls:
    recent_do = next((do for do in dos if do < mulpos), 0)
    recent_dont = next((dont for dont in donts if dont < mulpos), -1)
    if recent_do > recent_dont:
        mulsum += trymul(mem[mulpos:])

print(mulsum)
