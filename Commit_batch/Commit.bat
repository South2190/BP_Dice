@echo off

cd %~dp0\..

git pull origin master
python Commit_batch/rewrite_json.py
git add .
git commit -a

:confirmation
set /p Slt="masterブランチへpushしますか?(y/n)>"
if '%Slt%' == 'y' (
	git push origin master
) else if not '%Slt%' == 'n' (
	goto confirmation
)

echo "完了しました"
pause