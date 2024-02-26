import datetime
import json
import sys

args = sys.argv

with open('settings.json', 'r') as f:
	settings = json.load(f)

settings['CommitDate'] = datetime.date.today().strftime('%Y-%m-%d')

if len(args) >= 3 and args[1] == 'tag':
	settings['Version'] = args[2]

with open('settings.json', 'w') as f:
	json.dump(settings, f, indent = 4)