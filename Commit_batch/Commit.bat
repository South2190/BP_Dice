@echo off

set Branch=dev

cd %~dp0\..

git pull origin %Branch%

:createtag
set /p Slt="tag���쐬���܂���?(y/n)>"
if '%Slt%' == 'y' (
	setlocal enabledelayedexpansion
	call:setversion
	python Commit_batch/rewrite_json.py tag !Ver!
) else if '%Slt%' == 'n' (
	python Commit_batch/rewrite_json.py
) else goto createtag
pause
git add .
git commit -a
goto confirmation

:setversion
set /p Ver="�o�[�W���������>"
if not defined Ver goto setversion
exit /b

:confirmation
set Slt=
set /p Slt="%Branch%�u�����`��push���܂���?(y/n)>"
if '%Slt%' == 'y' (
	git push origin %Branch%
) else if not '%Slt%' == 'n' (
	goto confirmation
)

if defined Ver (
	git tag -a !Ver!
	git push origin !Ver!
	endlocal
)

echo �������܂���
pause