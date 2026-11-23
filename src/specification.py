"""Спецификация команд учебной виртуальной машины, вариант 34."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandSpec:
    """Код операции, число бит операнда и длина машинной команды."""

    opcode: int
    operand_bits: int
    size: int


@dataclass(frozen=True)
class Instruction:
    """Промежуточное представление команды ассемблера."""

    mnemonic: str
    operand: int | None = None


OPCODE_BITS = 7
COMMANDS = {
    "LOAD": CommandSpec(87, 18, 4),
    "READ": CommandSpec(63, 0, 1),
    "STORE": CommandSpec(39, 29, 5),
    "OR": CommandSpec(1, 29, 5),
}
BY_OPCODE = {spec.opcode: name for name, spec in COMMANDS.items()}
MAX_ADDRESS = (1 << 29) - 1


def format_fields(instruction: Instruction) -> str:
    """Показать поля инструкции в формате проверочного задания."""
    spec = COMMANDS[instruction.mnemonic]
    fields = f"A={spec.opcode}"
    if instruction.operand is not None:
        fields += f", B={instruction.operand}"
    return fields
