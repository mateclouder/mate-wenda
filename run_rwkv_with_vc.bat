@echo off
call  "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
set RWKV_CUDA_ON=1
:a
python wenda.py -t rwkv
goto a
pause
exit /b