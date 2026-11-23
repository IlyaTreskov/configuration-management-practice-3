#!/usr/bin/env sh
set -eu
case "${1:-}" in
  test) python -m unittest discover -s tests -v ;;
  spec) python -m src.assembler examples/spec_tests.asm build/spec_tests.bin --test ;;
  *) echo "Использование: sh run.sh test|spec"; exit 1 ;;
esac
