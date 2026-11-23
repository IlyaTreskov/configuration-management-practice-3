"""Интерпретатор УВМ варианта 34 с раздельными областями памяти."""

import argparse
import csv
from dataclasses import dataclass, field
from pathlib import Path

from src.machine_code import decode_instruction
from src.specification import MAX_ADDRESS, Instruction


@dataclass
class Machine:
    """Состояние машины: бинарная программа, данные, аккумулятор и PC."""

    program: bytes
    memory: dict[int, int] = field(default_factory=dict)
    accumulator: int = 0
    pc: int = 0

    def check_address(self, address: int) -> None:
        """Ограничить адреса разрядностью архитектуры."""
        if not 0 <= address <= MAX_ADDRESS:
            raise ValueError(f"Неверный адрес памяти: {address}")

    def read(self, address: int) -> int:
        """Прочитать ячейку данных; незаписанные ячейки равны нулю."""
        self.check_address(address)
        return self.memory.get(address, 0)

    def write(self, address: int, value: int) -> None:
        """Записать значение в ячейку памяти данных."""
        self.check_address(address)
        self.memory[address] = value

    def execute(self, instruction: Instruction) -> None:
        """Выполнить одну базовую инструкцию."""
        operand = instruction.operand
        if instruction.mnemonic == "LOAD":
            self.accumulator = operand
        elif instruction.mnemonic == "READ":
            self.accumulator = self.read(self.accumulator)
        elif instruction.mnemonic == "STORE":
            self.write(operand, self.accumulator)
        else:
            raise ValueError("Команда пока не реализована")

    def run(self) -> int:
        """Считывать, декодировать и исполнять команды до конца файла."""
        count = 0
        while self.pc < len(self.program):
            instruction, self.pc = decode_instruction(self.program, self.pc)
            self.execute(instruction)
            count += 1
        return count


def write_dump(
    memory: dict[int, int], output: Path, start: int, end: int
) -> None:
    """Выгрузить включительный диапазон адресов памяти в CSV."""
    if not 0 <= start <= end <= MAX_ADDRESS:
        raise ValueError("Некорректный диапазон адресов памяти")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["address", "value"])
        for address in range(start, end + 1):
            writer.writerow([address, memory.get(address, 0)])


def main() -> None:
    """Запустить исполнение бинарного файла и сохранить дамп."""
    parser = argparse.ArgumentParser(description="Интерпретатор УВМ №34")
    parser.add_argument("binary", type=Path, help="Бинарная программа")
    parser.add_argument("dump", type=Path, help="Выходной CSV")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()
    try:
        machine = Machine(args.binary.read_bytes())
        count = machine.run()
        write_dump(machine.memory, args.dump, args.start, args.end)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Выполнено команд: {count}")
    print(f"Аккумулятор: {machine.accumulator}")
    print(f"Дамп сохранён: {args.dump}")


if __name__ == "__main__":
    main()
