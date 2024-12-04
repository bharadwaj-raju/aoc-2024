from collections.abc import Iterable, Generator
from util import readtext

DEBUG = False


def expect_num(mem: str, pos: int) -> tuple[int, int]:
    digits: list[str] = []
    while mem[pos] in "1234567890":
        digits.append(mem[pos])
        pos += 1
    return (int("".join(digits)), pos)


def expect(mem: str, pos: int, ation: str) -> int:
    if not mem[pos:].startswith(ation):
        if DEBUG:
            print(f"expected {ation} at {pos} [context: {mem[pos-1:pos+10]!r}]")
        raise ValueError
    return pos + len(ation)


def maybe(mem: str, pos: int, s: str) -> int:
    try:
        return expect(mem, pos, s)
    except ValueError:
        return pos


def expect_func_args(mem: str, pos: int, nargs: int) -> tuple[list[int], int]:
    # called after parsing the (
    args: list[int] = []
    for i in range(nargs):
        num, pos = expect_num(mem, pos)
        args.append(num)
        if i != nargs - 1:
            pos = expect(mem, pos, ",")
    pos = expect(mem, pos, ")")
    return (args, pos)


def expect_func(mem: str, pos: int, name: str, nargs: int) -> tuple[list[int], int]:
    pos = expect(mem, pos, name + "(")
    args, pos = expect_func_args(mem, pos, nargs)
    return (args, pos)


KNOWN_COMMANDS = {
    "do": 0,
    "don't": 0,
    "mul": 2,
}


def parse(mem: str) -> Generator[tuple[str, list[int]]]:
    pos = 0
    while pos < len(mem):
        for cmd, nargs in KNOWN_COMMANDS.items():
            try:
                args, pos = expect_func(mem, pos, cmd, nargs)
                yield (cmd, args)
                break
            except (IndexError, ValueError) as e:
                pass
        else:
            pos += 1


def execute(commands: Iterable[tuple[str, list[int]]]) -> int:
    enabled = True
    mulsum = 0
    for cmd in commands:
        match cmd:
            case ("do", []):
                enabled = True
            case ("don't", []):
                enabled = False
            case ("mul", [a, b]):
                if enabled:
                    mulsum += a * b
    return mulsum


print(execute(parse(readtext())))
