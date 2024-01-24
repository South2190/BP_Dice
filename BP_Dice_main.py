import datetime
import discord
import json
import os
import platform
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

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="/dice"))
	LOG.info("Botの起動が完了しました")

@bot.slash_command(description="ダイスを振ります（範囲：0～999）")
async def dice(ctx):
	dicenum = random.randint(0, 999)
	await ctx.respond("ダイス！【{}】".format(dicenum))
	men = await bot.fetch_user(ctx.author.id)
	LOG.debug("{} rolled the dice -> {}".format(men, dicenum))

@bot.event
async def on_error():
	LOG.exception("例外が発生しました")

# 設定ファイルのオープン
with open('settings.json', 'r') as f:
	settings = json.load(f)

# タイトルの設定
titletext = "BP_Dice CommitDate:" + settings['CommitDate']
title(titletext)

# ログファイル出力先のディレクトリが存在しない場合作成する
if os.path.isdir(settings['LoggingDirectoryName']) == False:
	os.mkdir(settings['LoggingDirectoryName'])

# ログファイル名の設定
logfilepath = settings['LoggingDirectoryName'] + "/" + datetime.date.today().strftime('%Y-%m-%d') + ".log"
settings["LoggingConfigulation"]["handlers"]["file"]["filename"] = logfilepath

config.dictConfig(settings["LoggingConfigulation"])
LOG = getLogger(__name__)

LOG.info("****************************************")
LOG.info(titletext)
LOG.debug("")
LOG.debug("version info:")
LOG.debug("python -> {}".format(platform.python_version()))
LOG.debug("pycord -> {}".format(discord.__version__))
LOG.info("****************************************")

bot.run(BP_Dice_token.DiscordBotToken)