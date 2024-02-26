import sys

args = sys.argv

if len(args) >= 3 and args[1] == 'tag':
	print(args[2])