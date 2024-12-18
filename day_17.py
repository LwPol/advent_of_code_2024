Registers = tuple[int, int, int]


class Program:
    def __init__(self, registers: Registers, code: list[int]):
        self.reg_a, self.reg_b, self.reg_c = registers
        self._code = code
        self._pc = 0
    
    def run(self) -> list[int]:
        output = []
        while self._pc < len(self._code):
            opcode = self._code[self._pc]
            operand = self._code[self._pc + 1]
            if opcode == 0:
                self.reg_a = self.__divide_op(operand)
            elif opcode == 1:
                self.reg_b ^= operand
            elif opcode == 2:
                self.reg_b = self.__combo_value(operand) % 8
            elif opcode == 3:
                if self.reg_a != 0:
                    self._pc = operand
                    continue
            elif opcode == 4:
                self.reg_b ^= self.reg_c
            elif opcode == 5:
                output.append(self.__combo_value(operand) % 8)
            elif opcode == 6:
                self.reg_b = self.__divide_op(operand)
            elif opcode == 7:
                self.reg_c = self.__divide_op(operand)
            self._pc += 2
        return output
    
    def reset(self):
        self._pc = 0
        self.reg_b = 0
        self.reg_c = 0

    def __divide_op(self, operand: int) -> int:
        return self.reg_a // (2 ** self.__combo_value(operand))
    
    def __combo_value(self, operand: int) -> int:
        if operand <= 3:
            return operand
        if operand == 4:
            return self.reg_a
        if operand == 5:
            return self.reg_b
        if operand == 6:
            return self.reg_c


def parse_input(lines: list[str]) -> tuple[Registers, list[int]]:
    register_line_length = len('Register A: ')
    reg_a = int(lines[0][register_line_length:])
    reg_b = int(lines[1][register_line_length:])
    reg_c = int(lines[2][register_line_length:])

    program = map(int, lines[4][len('Program: '):].split(','))
    return (reg_a, reg_b, reg_c), list(program)


def octals_to_number(octals: list[int]) -> int:
    if not octals:
        return 0
    return int(''.join(bin(o)[2:].zfill(3) for o in octals), 2)


def construct_impl(program: Program, sequence: list[int], octals: list[int]) -> bool:
    if not sequence:
        return True

    next_num = sequence[0]
    for i in range(8):
        program.reset()
        program.reg_a = octals_to_number(octals + [i])
        if program.run() == [next_num]:
            octals.append(i)
            if construct_impl(program, sequence[1:], octals):
                return True
            else:
                octals.pop()
    return False
    


def construct_reg_a_value_for_output(code: list[int]) -> str:
    octals = []
    # get rid of last jump instruction in code
    debug_program = Program((0, 0, 0), code[:-2])
    if construct_impl(debug_program, list(reversed(code)), octals):
        return octals_to_number(octals)
    raise RuntimeError('Failed to find proper sequence')


def resolve_part1(input):
    out = Program(*parse_input(input)).run()
    return ','.join(map(str, out))

def resolve_part2(input):
    _, code = parse_input(input)
    return construct_reg_a_value_for_output(code)