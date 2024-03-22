@echo off

set EDITOR=sublime_text.exe
for /f "DELIMS=" %%A in ('tasklist ^| find /c "%EDITOR%"') do set EDITORP=%%A
if %EDITORP% gtr 0 echo ！！！　エディターの終了を確認してください　！！！

cd %~dp0
python rewrite_json.py

echo 完了しました
pause