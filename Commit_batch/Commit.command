#!/bin/bash

cd `dirname $0`/..

git pull origin master
python Commit_batch/rewrite_json.py
git add .
git commit -a

while true
do
echo -n "masterブランチへpushしますか?(y/n)>"
read Slt

if [ ${Slt} = "y" ]; then
	git push origin master
	break
elif [ ${Slt} = "n" ]; then
	break
fi
done

echo "完了しました"
read