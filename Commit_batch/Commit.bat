@echo off
cd %~dp0\..

git pull origin master
git add .
git commit -a

:confirmation
set yn = nul
set /p yn="master�u�����`��push���܂���?(y/n)>"
if '%yn%' == 'y' (
	git push origin master
) else if not '%yn%' == 'n' (
	goto confirmation
)
pause
goto :eof