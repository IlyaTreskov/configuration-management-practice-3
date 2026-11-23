"""Проверки этапа 3: память и копирование массива."""

import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.assembler import parse_source
from src.interpreter import Machine, write_dump
from src.machine_code import decode_instruction, encode_program


class InterpreterTests(unittest.TestCase):
    """Проверяет исполнение основных команд УВМ."""

    def test_decoding_reference_bytes(self):
        """Декодер восстанавливает все поля из бинарного файла."""
        program = parse_source("LOAD 180\nREAD\nSTORE 643\nOR 410")
        machine_code = encode_program(program)
        offset = 0
        decoded = []
        while offset < len(machine_code):
            instruction, offset = decode_instruction(machine_code, offset)
            decoded.append(instruction)
        self.assertEqual(decoded, program)

    def test_copy_array(self):
        """Копирование трёх значений сохраняет источник и назначение."""
        source = Path("examples/copy_array.asm").read_text(encoding="utf-8")
        code = encode_program(parse_source(source))
        machine = Machine(code)
        self.assertEqual(machine.run(), 15)
        self.assertEqual(
            [machine.read(index) for index in range(100, 106)],
            [10, 20, 30, 10, 20, 30],
        )

    def test_dump(self):
        """Дамп содержит адреса и значения в формате CSV."""
        with TemporaryDirectory() as folder:
            output = Path(folder) / "memory.csv"
            write_dump({100: 10, 101: 20}, output, 100, 102)
            with output.open(encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))
        self.assertEqual(rows, [
            ["address", "value"], ["100", "10"],
            ["101", "20"], ["102", "0"],
        ])

    def test_invalid_machine_code(self):
        """Неизвестная и обрезанная команда отклоняются."""
        with self.assertRaises(ValueError):
            Machine(bytes([0])).run()
        with self.assertRaises(ValueError):
            Machine(bytes([87, 0])).run()

    def test_separated_memories(self):
        """Запись в память данных не меняет память команд."""
        code = encode_program(parse_source("LOAD 7\nSTORE 0"))
        machine = Machine(code)
        machine.run()
        self.assertEqual(machine.program, code)
        self.assertEqual(machine.read(0), 7)
