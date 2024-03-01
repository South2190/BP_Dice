import datetime
import json
import os

branch = "dev"

os.chdir("..")
os.system("git pull origin {}".format(branch))

with open('settings.json', 'r') as f:
	settings = json.load(f)

settings['CommitDate'] = datetime.date.today().strftime('%Y-%m-%d')

Slt = ""
while(not Slt):
	Slt = input("tagを作成しますか?(y/n)>")
if Slt == 'y':
	Ver = ""
	while(not Ver):
		Ver = input("バージョンを入力>")
		settings['Version'] = Ver

with open('settings.json', 'w') as f:
	json.dump(settings, f, indent = 4)

os.system("git add .")
os.system("git commit -a")

Slt = ""
while(not Slt):
	Slt = input("{}ブランチへpushしますか?(y/n)>".format(branch))
if Slt == 'y':
	os.system("git push origin {}".format(branch))

if Ver:
	os.system("git tag -a {}".format(Ver))
	os.system("git push origin {}".format(Ver))