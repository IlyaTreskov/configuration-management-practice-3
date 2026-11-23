#!/usr/bin/env sh
set -eu
case "${1:-}" in
  test) python -m unittest discover -s tests -v ;;
  spec) python -m src.assembler examples/spec_tests.asm \
    build/spec_tests.bin --test ;;
  copy) python -m src.assembler examples/copy_array.asm \
    build/copy_array.bin && python -m src.interpreter \
    build/copy_array.bin build/copy_array.csv --start 100 --end 105 ;;
  or) python -m src.assembler examples/bitwise_or.asm \
    build/bitwise_or.bin && python -m src.interpreter \
    build/bitwise_or.bin build/bitwise_or.csv --start 300 --end 301 ;;
  *) echo "Использование: sh run.sh test|spec|copy|or"; exit 1 ;;
esac
