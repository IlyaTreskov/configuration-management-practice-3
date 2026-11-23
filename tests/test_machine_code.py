"""Проверки этапа 2: байтовая упаковка инструкций."""

import unittest

from src.assembler import parse_source
from src.machine_code import encode_instruction, encode_program
from src.specification import Instruction


class MachineCodeTests(unittest.TestCase):
    """Проверяет точные эталонные байты варианта 34."""

    def test_bytes_from_specification(self):
        """Все четыре эталонные последовательности совпадают."""
        fixtures = [
            (Instruction("LOAD", 180), bytes.fromhex("57 5A 00 00")),
            (Instruction("READ"), bytes.fromhex("3F")),
            (Instruction("STORE", 643), bytes.fromhex("A7 41 01 00 00")),
            (Instruction("OR", 410), bytes.fromhex("01 CD 00 00 00")),
        ]
        for instruction, expected in fixtures:
            with self.subTest(instruction=instruction):
                self.assertEqual(encode_instruction(instruction), expected)

    def test_file_length(self):
        """Общая длина файла равна сумме длин команд."""
        commands = parse_source("LOAD 180\nREAD\nSTORE 643\nOR 410")
        self.assertEqual(len(encode_program(commands)), 15)

    def test_large_operand(self):
        """Максимальный адрес корректно укладывается в 29 бит."""
        code = encode_instruction(Instruction("STORE", (1 << 29) - 1))
        self.assertEqual(len(code), 5)
