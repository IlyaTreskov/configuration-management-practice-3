"""Проверки этапа 4: побитовое ИЛИ."""

from pathlib import Path
import unittest

from src.assembler import parse_source
from src.interpreter import Machine
from src.machine_code import encode_program


class AluTests(unittest.TestCase):
    """Проверяет результаты бинарной операции над аккумулятором."""

    def test_or_example(self):
        """Операция 12 | 10 даёт 14, результат сохраняется в память."""
        source = Path("examples/bitwise_or.asm").read_text(
            encoding="utf-8"
        )
        machine = Machine(encode_program(parse_source(source)))
        self.assertEqual(machine.run(), 5)
        self.assertEqual(machine.read(300), 12)
        self.assertEqual(machine.read(301), 14)
        self.assertEqual(machine.accumulator, 14)

    def test_or_with_zero_and_other_values(self):
        """Побитовое ИЛИ работает для разных целых чисел."""
        for first, second, expected in ((5, 2, 7), (15, 0, 15)):
            with self.subTest(first=first, second=second):
                source = (
                    f"LOAD {first}\nSTORE 8\n"
                    f"LOAD {second}\nOR 8\nSTORE 9"
                )
                machine = Machine(encode_program(parse_source(source)))
                machine.run()
                self.assertEqual(machine.read(9), expected)
