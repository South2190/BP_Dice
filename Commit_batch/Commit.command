#!/bin/bash

cd `dirname $0`/..

git pull origin dev
python Commit_batch/rewrite_json.py
git add .
git commit -a

while true
do
echo -n "devブランチへpushしますか?(y/n)>"
read Slt

if [ ${Slt} = "y" ]; then
	git push origin dev
	break
elif [ ${Slt} = "n" ]; then
	break
fi
done

echo "完了しました"
read