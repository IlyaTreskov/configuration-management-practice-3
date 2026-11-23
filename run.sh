#!/usr/bin/env sh
set -eu
case "${1:-}" in
  test) python -m unittest discover -s tests -v ;;
  spec) python -m src.assembler examples/spec_tests.asm \
    build/spec_tests.bin --test ;;
  copy) python -m src.assembler examples/copy_array.asm \
    build/copy_array.bin && python -m src.interpreter \
    build/copy_array.bin build/copy_array.csv --start 100 --end 105 ;;
  *) echo "Использование: sh run.sh test|spec|copy"; exit 1 ;;
esac
