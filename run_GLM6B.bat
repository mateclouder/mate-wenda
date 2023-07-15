@echo off
%~d0
cd %~dp0
:a
python wenda.py -t glm6b
goto a
pause
exit /b