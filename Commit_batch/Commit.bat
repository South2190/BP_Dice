@echo off
cd %~dp0\..

git pull origin master
git add .
git commit -a

:confirmation
set /p yn = master�u�����`��push���܂���?(y/n)^>
if '%yn%' == 'y' (
	git push origin master
	pause
	goto :eof
) else if '%yn%' == 'n' (
	pause
	goto :eof
)
goto confirmation