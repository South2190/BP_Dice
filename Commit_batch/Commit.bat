@echo off

cd %~dp0\..

git pull origin dev
python Commit_batch/rewrite_json.py
git add .
git commit -a

:confirmation
set /p Slt="devブランチへpushしますか?(y/n)>"
if '%Slt%' == 'y' (
	git push origin dev
) else if not '%Slt%' == 'n' (
	goto confirmation
)

echo "完了しました"
pause