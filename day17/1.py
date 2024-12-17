from collections.abc import Sequence

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


def combo(registers: dict[str, int], operand: int) -> int:
    if operand == 7:
        raise ValueError("7 is reserved!")
    if 0 <= operand <= 3:
        return operand
    return registers["ABC"[operand - 4]]


def compute(registers: dict[str, int], program: Sequence[int]) -> tuple[list[int], dict[str, int]]:
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
            registers["B"] = registers["B"] ^ operand
            ip += 2
        elif op == "bst":
            c = combo(registers, operand)
            registers["B"] = c % 8
            ip += 2
        elif op == "jnz":
            if registers["A"] != 0:
                ip = operand
            else:
                ip += 2
        elif op == "bxc":
            registers["B"] = registers["B"] ^ registers["C"]
            ip += 2
        elif op == "out":
            c = combo(registers, operand)
            output.append(c % 8)
            ip += 2
        elif op.endswith("dv"):
            c = combo(registers, operand)
            dest = op[0].upper()
            registers[dest] = registers["A"] // (2**c)
            ip += 2
    return (output, registers)


registers, program = readgroups()
registers = {reg.split(": ")[0][-1]: int(reg.split(": ")[-1]) for reg in registers}
program = [int(x) for x in program[0].split(": ")[-1].split(",")]

output, final_registers = compute(registers, program)

print(output)
