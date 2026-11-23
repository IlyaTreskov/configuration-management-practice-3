"""Проверки этапа 1: разбор исходного текста."""

import unittest

from src.assembler import parse_source
from src.specification import Instruction, format_fields


class ParserTests(unittest.TestCase):
    """Проверяет синтаксис и промежуточное представление."""

    def test_specification_fields(self):
        """Поля совпадают с приведёнными в методичке."""
        source = "LOAD 180\nREAD\nSTORE 643\nOR 410"
        result = [format_fields(item) for item in parse_source(source)]
        self.assertEqual(result, [
            "A=87, B=180", "A=63", "A=39, B=643", "A=1, B=410",
        ])

    def test_comments_and_spacing(self):
        """Комментарии и пробелы не мешают разбору."""
        self.assertEqual(parse_source("  load 0x10 # x\n; x\nread"), [
            Instruction("LOAD", 16), Instruction("READ"),
        ])

    def test_invalid_operands(self):
        """Недопустимые параметры приводят к ошибке."""
        for source in ("LOAD -1", "LOAD 262144", "OR 536870912",
                       "READ 1", "STORE", "OOPS 1"):
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    parse_source(source)
