import discord
import json
import os
import random
from logging import getLogger, config

import BP_Dice_token

bot = discord.Bot()

# ウインドウタイトルの設定
def title(text):
    # OSの種類を判別する
    # Windows
	if os.name == 'nt':
		os.system(f'title {text}')
    # Mac / Linux
	elif os.name == 'posix':
		print(f'\x1b]2;{text}\x07', end='', flush=True)

# 

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="/dice"))

@bot.slash_command(description="ダイスを振ります（範囲：0～999）")
async def dice(ctx):
	await ctx.respond('ダイス！【{}】'.format(random.randint(0, 999)))

title("BP_Dice")

with open('settings.json', 'r') as f:
	settings = json.load(f)
print("****************************************")
print("BP_Dice")
print("CommitDate:{}".format(settings['CommitDate']))
print("****************************************")
bot.run(BP_Dice_token.DiscordBotToken)