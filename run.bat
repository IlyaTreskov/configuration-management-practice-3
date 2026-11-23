@echo off
if /I "%~1"=="test" goto test
if /I "%~1"=="spec" goto spec
if /I "%~1"=="copy" goto copy
echo Использование: run.bat test^|spec^|copy
exit /b 1
:test
python -m unittest discover -s tests -v
exit /b %ERRORLEVEL%
:spec
python -m src.assembler examples/spec_tests.asm build/spec_tests.bin --test
exit /b %ERRORLEVEL%
:copy
python -m src.assembler examples/copy_array.asm build/copy_array.bin
if errorlevel 1 exit /b %ERRORLEVEL%
python -m src.interpreter build/copy_array.bin build/copy_array.csv --start 100 --end 105
exit /b %ERRORLEVEL%
