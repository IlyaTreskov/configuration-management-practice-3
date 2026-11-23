"""Ассемблер УВМ варианта 34; запуск через python -m src.assembler."""

import argparse
from pathlib import Path

from src.specification import COMMANDS, Instruction, format_fields


def parse_line(line: str, number: int) -> Instruction | None:
    """Преобразовать одну строку исходного файла в команду УВМ."""
    clean = line.split("#", 1)[0].split(";", 1)[0].strip()
    if not clean:
        return None
    parts = clean.replace(",", " ").split()
    name = parts[0].upper()
    if name not in COMMANDS:
        raise ValueError(f"Строка {number}: неизвестная команда {name}")
    spec = COMMANDS[name]
    if spec.operand_bits == 0:
        if len(parts) != 1:
            raise ValueError(f"Строка {number}: {name} без операнда")
        return Instruction(name)
    if len(parts) != 2:
        raise ValueError(f"Строка {number}: {name} требует один операнд")
    try:
        operand = int(parts[1], 0) if parts[1].lower().startswith(
            ("0x", "0b", "0o")
        ) else int(parts[1])
    except ValueError as error:
        raise ValueError(f"Строка {number}: неверное число") from error
    if not 0 <= operand < (1 << spec.operand_bits):
        raise ValueError(f"Строка {number}: операнд вне диапазона")
    return Instruction(name, operand)


def parse_source(source: str) -> list[Instruction]:
    """Получить промежуточное представление всей программы."""
    program = []
    for number, line in enumerate(source.splitlines(), start=1):
        instruction = parse_line(line, number)
        if instruction is not None:
            program.append(instruction)
    return program


def main() -> None:
    """Обработать аргументы командной строки (этап 1)."""
    parser = argparse.ArgumentParser(description="Ассемблер УВМ №34")
    parser.add_argument("source", type=Path, help="Исходный файл .asm")
    parser.add_argument("output", type=Path, help="Будущий бинарный файл")
    parser.add_argument("--test", action="store_true", help="Вывод полей")
    args = parser.parse_args()
    try:
        program = parse_source(args.source.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Разобрано команд: {len(program)}")
    if args.test:
        for instruction in program:
            print(format_fields(instruction))
    print("Этап 1: промежуточное представление получено")


if __name__ == "__main__":
    main()
