@echo off

set EDITOR=sublime_text.exe
for /f "DELIMS=" %%A in ('tasklist ^| find /c "%EDITOR%"') do set EDITORP=%%A
if %EDITORP% gtr 0 echo �I�I�I�@�G�f�B�^�[�̏I�����m�F���Ă��������@�I�I�I

cd %~dp0
python rewrite_json.py

echo �������܂���
pause