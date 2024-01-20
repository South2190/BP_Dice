import datetime
import json

with open('settings.json', 'r') as f:
	settings = json.load(f)

settings['CommitDate'] = datetime.date.today().strftime('%Y-%m-%d')

with open('settings.json', 'w') as f:
	json.dump(settings, f, indent = 4)