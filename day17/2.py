from collections.abc import Sequence
from itertools import batched, product

from util import readgroups

operations = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: "out",
    6: "bdv",
    7: "cdv",
}


def o(x):
    return oct(x)[2:]


combo_opcodes = ("bst", "out", "adv", "bdv", "cdv")


def combo_repr(operand: int) -> str | int:
    if 0 <= operand <= 3:
        return operand
    return "ABC"[operand - 4]


def disassemble(program: Sequence[int]) -> list[tuple[str, str | int]]:
    assembly = []
    for opcode, operand in batched(program, 2):
        name = operations[opcode]
        if name in combo_opcodes:
            operand = combo_repr(operand)
        assembly.append((name, operand))
    return assembly


def combo(registers: dict[str, int], operand: int) -> int:
    if operand == 7:
        raise ValueError("7 is reserved!")
    if 0 <= operand <= 3:
        return operand
    return registers["ABC"[operand - 4]]


def compute(registers: dict[str, int], program: Sequence[int], verbose=False) -> tuple[list[int], dict[str, int]]:
    def log(*args):
        if verbose:
            print(*args)

    registers = registers.copy()
    output = []
    ip = 0
    while ip < len(program):
        try:
            opcode = program[ip]
            operand = program[ip + 1]
        except IndexError:
            print("out of bounds read")
            return (output, registers)
        op = operations[opcode]
        if op == "bxl":
            log(f"B = {o(registers['B'])} ^ {o(operand)} = {o(registers['B'] ^ operand)}")
            registers["B"] = registers["B"] ^ operand
            ip += 2
        elif op == "bst":
            c = combo(registers, operand)
            log(f"B = {combo_repr(operand)} % 8 = {o(c)} % 8 = {o(c % 8)}")
            registers["B"] = c % 8
            ip += 2
        elif op == "jnz":
            if registers["A"] != 0:
                log(f"JUMP 0 (A = {o(registers['A'])})")
                ip = operand
            else:
                ip += 2
        elif op == "bxc":
            log(f"B = B ^ C = {o(registers["B"])} ^ {o(registers["C"])} = {o(registers["B"] ^ registers["C"])}")
            registers["B"] = registers["B"] ^ registers["C"]
            ip += 2
        elif op == "out":
            c = combo(registers, operand)
            log(f"OUTPUT {combo_repr(operand)} = {o(c)} % 8 = {o(c % 8)}")
            output.append(c % 8)
            ip += 2
        elif op.endswith("dv"):
            c = combo(registers, operand)
            dest = op[0].upper()
            log(
                f"{dest} = A // (2^{combo_repr(operand)}) = {o(registers['A'])} // (2^{c}) = {o(registers['A'])} // {2**c} = {o(registers['A'] // 2**c)} ({registers['A'] // 2**c})"
            )
            registers[dest] = registers["A"] // (2**c)
            ip += 2
    return (output, registers)


registers, program = readgroups()
registers = {reg.split(": ")[0][-1]: int(reg.split(": ")[-1]) for reg in registers}
program = [int(x) for x in program[0].split(": ")[-1].split(",")]


# written based on disassembly, this will probably need to be modified for other inputs
def f(A, A_target):
    out = []
    while A != A_target:
        B = A % 8
        B = B ^ 1
        C = A // (2**B)
        B = B ^ 5
        B = B ^ C
        out.append(B % 8)
        A = A // 8
    return out


def find(code: int, A_target: int) -> list[int]:
    combs = []
    for comb in "01234567":
        # I find octal is easier to think in here since we're mostly dividing and modding by 8
        A = o(A_target) + comb
        A = int(A, 8)
        run = f(A, A_target)
        if run and run[-1] == code:
            combs.append(A)
    return combs


so_far = [[0]]
for code in program[::-1]:
    so_far.append([])
    for prev_possibility in so_far[-2]:
        A_target = prev_possibility
        for new_possibility in find(code, A_target):
            so_far[-1].append(new_possibility)

finals = so_far[-1]

for A in finals:
    registers["A"] = A
    out, _ = compute(registers, program)
    assert out == program

print(min(finals))
