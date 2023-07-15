@echo off
%~d0
cd %~dp0
cd ..
python plugins/gen_data_st.py
pause