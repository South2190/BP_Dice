@echo off

cd %~dp0\..

git pull origin master
python Commit_batch/rewrite_json.py
git add .
git commit -a

:confirmation
set /p yn="master�u�����`��push���܂���?(y/n)>"
if '%yn%' == 'y' (
	git push origin master
) else if not '%yn%' == 'n' (
	goto confirmation
)

pause
goto :eof