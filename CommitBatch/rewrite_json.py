import datetime
import json
import os

branch = "master"

os.chdir("..")
os.system("git pull origin {}".format(branch))

with open('settings.json', 'r', encoding = "utf-8") as f:
	settings = json.load(f)

settings['CommitDate'] = datetime.date.today().strftime('%Y-%m-%d')

Slt = ""
Ver = ""
while(not Slt):
	Slt = input("tagを作成しますか?(y/n)>")
if Slt == 'y':
	while(not Ver):
		Ver = input("バージョンを入力>")
		settings['Version'] = Ver

with open('settings.json', 'w', encoding = "utf-8") as f:
	json.dump(settings, f, indent = 4, ensure_ascii = False)

os.system("git add .")
print("コミットメッセージを入力してください . . .")
os.system("git commit -a")

Slt = ""
while(not Slt):
	Slt = input("{}ブランチへpushしますか?(y/n)>".format(branch))
if Slt == 'y':
	os.system("git push origin {}".format(branch))

if Ver:
	print("タグメッセージを入力してください . . .")
	os.system("git tag -a {}".format(Ver))
	os.system("git push origin {}".format(Ver))