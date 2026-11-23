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
    if spec.operand_bits == 0 and instruction.operand is not None:
        raise ValueError("У команды не должно быть операнда")
    if spec.operand_bits and instruction.operand is None:
        raise ValueError("Для команды требуется операнд")
    operand = instruction.operand or 0
    if not 0 <= operand < (1 << spec.operand_bits):
        raise ValueError("Операнд вне допустимого диапазона")
    packed = spec.opcode | (operand << OPCODE_BITS)
    return packed.to_bytes(spec.size, byteorder="little")


def encode_program(instructions: list[Instruction]) -> bytes:
    """Собрать бинарный файл из списка инструкций."""
    return b"".join(encode_instruction(item) for item in instructions)


def format_bytes(data: bytes) -> str:
    """Вывести байты в формате из спецификации УВМ."""
    return ", ".join(f"0x{value:02X}" for value in data)


def decode_instruction(data: bytes, offset: int = 0) -> tuple[Instruction, int]:
    """Прочитать одну машинную команду и вернуть новый указатель."""
    if not 0 <= offset < len(data):
        raise ValueError("Нет данных для чтения команды")
    opcode = data[offset] & ((1 << OPCODE_BITS) - 1)
    if opcode not in BY_OPCODE:
        raise ValueError(f"Неизвестный код операции: {opcode}")
    name = BY_OPCODE[opcode]
    spec = COMMANDS[name]
    end = offset + spec.size
    if end > len(data):
        raise ValueError("Обрезанная машинная команда")
    packed = int.from_bytes(data[offset:end], byteorder="little")
    valid_bits = OPCODE_BITS + spec.operand_bits
    if packed >> valid_bits:
        raise ValueError("Ненулевые зарезервированные биты")
    if spec.operand_bits == 0:
        return Instruction(name), end
    mask = (1 << spec.operand_bits) - 1
    operand = (packed >> OPCODE_BITS) & mask
    return Instruction(name, operand), end
