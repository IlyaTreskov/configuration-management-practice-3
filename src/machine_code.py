"""Преобразование команд УВМ в машинные байты и обратно."""

from src.specification import (
    BY_OPCODE,
    COMMANDS,
    OPCODE_BITS,
    Instruction,
)


def encode_instruction(instruction: Instruction) -> bytes:
    """Упаковать операцию и операнд в little-endian машинный код."""
    spec = COMMANDS[instruction.mnemonic]
    operand = instruction.operand or 0
    if not 0 <= operand < (1 << spec.operand_bits if
                            spec.operand_bits else 1):
        raise ValueError("Операнд вне допустимого диапазона")
    packed = spec.opcode | (operand << OPCODE_BITS)
    return packed.to_bytes(spec.size, byteorder="little")


def encode_program(instructions: list[Instruction]) -> bytes:
    """Собрать бинарный файл из списка инструкций."""
    return b"".join(encode_instruction(item) for item in instructions)


def format_bytes(data: bytes) -> str:
    """Вывести байты в формате из спецификации УВМ."""
    return ", ".join(f"0x{value:02X}" for value in data)
