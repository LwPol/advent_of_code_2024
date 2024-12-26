from typing import NamedTuple, Optional
from enum import Enum

Wires = dict[str, bool]

class LogicalGate(NamedTuple):
    lhs: str
    rhs: str
    operator: str
    output: str


class WireType(Enum):
    INTERMEDIATE_XOR = 0
    INTERMEDIATE_CARRY_FLAG = 1
    CARRY_FLAG = 2
    INPUT_WIRE = 3
    XORED_UNKNOWN = 4

WireCls = dict[str, WireType]


def parse_starting_inputs(lines: list[str]) -> Wires:
    def parse_one(line: str) -> tuple[str, bool]:
        wire, value = line.split(': ')
        return wire, int(value)
    return dict(map(parse_one, lines))


def parse_logical_gates(lines: list[str]) -> list[LogicalGate]:
    def parse_one(line: str) -> LogicalGate:
        tokens = line.split(' ')
        return LogicalGate(lhs=tokens[0], rhs=tokens[2], operator=tokens[1], output=tokens[4])
    return list(map(parse_one, lines))


def parse_input(lines: list[str]) -> tuple[Wires, list[LogicalGate]]:
    empty_line_idx = next(idx for idx, line in enumerate(lines) if not line)
    return (parse_starting_inputs(lines[:empty_line_idx]),
            parse_logical_gates(lines[empty_line_idx + 1:]))


def generate_output(lhs: bool, rhs: bool, operator: str) -> bool:
    if operator == 'AND':
        return lhs and rhs
    if operator == 'OR':
        return lhs or rhs
    if operator == 'XOR':
        return lhs ^ rhs
    raise RuntimeError('Unknown operator')


def run_gates(wires: Wires, gates: list[LogicalGate]) -> Optional[Wires]:
    wires = dict(wires)
    left = []
    while gates:
        for gate in gates:
            if gate.lhs in wires and gate.rhs in wires:
                wires[gate.output] = generate_output(wires[gate.lhs],
                                                     wires[gate.rhs],
                                                     gate.operator)
            else:
                left.append(gate)
        if len(gates) == len(left):
            return None
        gates = left
        left = []
    return wires


def decode_output_number(wires: Wires) -> int:
    result = 0
    for wire, value in filter(lambda w: w[0].startswith('z'), wires.items()):
        if value:
            result |= 1 << int(wire[1:])
    return result


def output_number(wires: Wires, gates: list[LogicalGate]) -> Optional[int]:
    after_exec = run_gates(wires, gates)
    return decode_output_number(after_exec) if after_exec is not None else None


def bit_number_to_wire(bit_no: int, prefix: str) -> str:
    return f'{prefix}{str(bit_no).zfill(2)}'


def is_input_wire(wire: str) -> bool:
    return wire.startswith('x') or wire.startswith('y')


def perform_initial_classification(gates: list[LogicalGate]) -> WireCls:
    def classify_gate(gate: LogicalGate) -> Optional[WireType]:
        if is_input_wire(gate.lhs) and is_input_wire(gate.rhs):
            return WireType.INPUT_WIRE
        if gate.operator == 'XOR':
            return WireType.XORED_UNKNOWN
        if gate.operator == 'OR':
            return WireType.INTERMEDIATE_CARRY_FLAG
        return None
    result = {}
    for gate in gates:
        wire_type = classify_gate(gate)
        if wire_type is not None:
            result[gate.lhs] = result[gate.rhs] = wire_type
    return result


def perform_secondary_classification(gates: list[LogicalGate],
                                     wire_types: WireCls) -> list[LogicalGate]:
    wrong_outputs = []
    for gate in filter(lambda g: is_input_wire(g.lhs) and is_input_wire(g.rhs), gates):
        if {gate.lhs, gate.rhs} == {'x00', 'y00'}:
            continue

        if gate.operator == 'XOR':
            if wire_types.get(gate.output) == WireType.XORED_UNKNOWN:
                wire_types[gate.output] = WireType.INTERMEDIATE_XOR
            else:
                wrong_outputs.append(gate)
        elif gate.operator == 'AND':
            if wire_types.get(gate.output) != WireType.INTERMEDIATE_CARRY_FLAG:
                wrong_outputs.append(gate)
    return wrong_outputs


def mark_carry_flags(wire_types: WireCls) -> None:
    keys = list(wire_types.keys())
    for key in keys:
        if wire_types[key] == WireType.XORED_UNKNOWN:
            wire_types[key] = WireType.CARRY_FLAG


def verify_intermediary_connections_by_type(gates: list[LogicalGate],
                                            wire_cls: WireCls,
                                            bits: int) -> list[LogicalGate]:
    wrong_outputs = []
    for gate in filter(lambda g: not is_input_wire(g.lhs), gates):
        if gate.operator == 'XOR':
            if not gate.output.startswith('z'):
                wrong_outputs.append(gate)
        elif gate.operator == 'AND':
            if wire_cls.get(gate.output) != WireType.INTERMEDIATE_CARRY_FLAG:
                wrong_outputs.append(gate)
        elif gate.operator == 'OR':
            if (wire_cls.get(gate.output) != WireType.CARRY_FLAG
                    and gate.output != bit_number_to_wire(bits, 'z')):
                wrong_outputs.append(gate)
    return wrong_outputs


def get_bits_count(wires: Wires) -> int:
    return max(int(wire[1:]) for wire in wires.keys()) + 1


def find_flawed_gates(wires: Wires, gates: list[LogicalGate]) -> list[LogicalGate]:
    wires_cls = perform_initial_classification(gates)
    bad_gates = perform_secondary_classification(gates, wires_cls)
    mark_carry_flags(wires_cls)
    bad_gates += verify_intermediary_connections_by_type(gates, wires_cls,
                                                         bits=get_bits_count(wires))
    # hopefully should be enough to find all invalid gates
    if len(bad_gates) != 8:
        raise RuntimeError('Did not find all flawed gates')
    return bad_gates


def get_incorrectly_attached_wires(wires: Wires, gates: list[LogicalGate]) -> list[str]:
    return [gate.output for gate in find_flawed_gates(wires, gates)]


def resolve_part1(input):
    return output_number(*parse_input(input))

def resolve_part2(input):
    wires = get_incorrectly_attached_wires(*parse_input(input))
    return ','.join(sorted(wires))
