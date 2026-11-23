@echo off
if /I "%~1"=="test" goto test
if /I "%~1"=="spec" goto spec
echo Использование: run.bat test^|spec
exit /b 1
:test
python -m unittest discover -s tests -v
exit /b %ERRORLEVEL%
:spec
python -m src.assembler examples/spec_tests.asm build/spec_tests.bin --test
exit /b %ERRORLEVEL%
