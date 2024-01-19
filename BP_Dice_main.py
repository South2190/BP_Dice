import discord
import os
import random

import BP_Dice_resource

bot = discord.Bot()

def title(text):
    # OSの種類を判別する
    # Windows
	if os.name == 'nt':
		os.system(f'title {text}')
    # Mac / Linux
	elif os.name == 'posix':
		print(f'\x1b]2;{text}\x07', end='', flush=True)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="/dice"))

@bot.slash_command(description="ダイスを振ります(範囲：0～999)")
async def dice(ctx):
	await ctx.respond('ダイス！【{}】'.format(random.randint(0, 999)))

title("BP_Dice v1.0.0")
bot.run(BP_Dice_resource.DiscordBotToken)