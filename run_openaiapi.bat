@echo off
set OPENAI_API_KEY=123
:a
python wenda.py -t openai
goto a
pause
exit /b