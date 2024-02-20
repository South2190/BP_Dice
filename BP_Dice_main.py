import datetime
import discord
from discord import Option
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

# Bot起動時の処理
@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name="/dice"))
	LOG.info("Botの起動が完了しました")

# diceコマンドの定義
@bot.slash_command(description="ダイスを振ります（範囲：0～999）")
async def dice(ctx):
	dicenum = random.randint(0, 999)
	await ctx.respond("ダイス！【{}】".format(dicenum))
	men = await bot.fetch_user(ctx.author.id)
	LOG.debug("{} rolled the dice -> {}".format(men, dicenum))

# cpcalcコマンドの定義
@bot.slash_command(description="コネクトクーポンの残り有効期限から日付を計算します")
async def cpcalc(
	ctx: discord.ApplicationContext,
	day: Option(int, description="残り日数"),
	hour: Option(int, description="残り時間数", required=False, default=0),
	minute: Option(int, description="残り分数", required=False, default=0)
):
	nowdate = datetime.datetime.now()
	calcresult = nowdate + datetime.timedelta(days=day, hours=hour, minutes=minute)
	if all([hour == 0, minute == 0]):
		resultfmt = '%m/%d'
	elif minute == 0:
		resultfmt = '%m/%d %H:00'
	else:
		resultfmt = '%m/%d %H:%M'
	await ctx.respond("`{}まで`".format(calcresult.strftime(resultfmt)), ephemeral=True)
	men = await bot.fetch_user(ctx.author.id)
	LOG.debug("{} calculated the date. nowdate:{} + (day:{}, hour:{}, minute:{}) -> {}".format(men, nowdate.strftime('%m/%d %H:%M'), day, hour, minute, calcresult.strftime(resultfmt)))

@bot.event
async def on_command_error(ctx, error):
	LOG.exception("エラーが発生しました")

# 設定ファイルのオープン
with open('settings.json', 'r') as f:
	settings = json.load(f)

# タイトルの設定
titletext = "BP_Dice CommitDate:" + settings['CommitDate']
title(titletext)

# ログファイル出力先のディレクトリが存在しない場合作成する
if os.path.isdir('log') == False:
	os.mkdir('log')

# ログファイル名の設定
logfilepath = "log/" + datetime.date.today().strftime('%Y-%m-%d') + ".log"
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