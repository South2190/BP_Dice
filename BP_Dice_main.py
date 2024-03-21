import datetime
import discord
from discord import Option
import json
import os
import platform
import random
import time
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
	await bot.change_presence(activity=discord.Game(name="/dice /cpcalc"))
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
	day: Option(int, description="残り日数", required=False, default=0),
	hour: Option(int, description="残り時間数", required=False, default=0),
	minute: Option(int, description="残り分数", required=False, default=0)
):
	nowdate = datetime.datetime.now()
	restext = ""
	resultfmt = '%m/%d %H:%M'
	# 引数の指定が無い場合は自動的に30日後の翌4時で計算する
	if all([day == 0, hour == 0, minute == 0]):
		work = nowdate + datetime.timedelta(days=31) if nowdate.hour >= 4 else nowdate + datetime.timedelta(days=30)
		calcresult = datetime.datetime(work.year, work.month, work.day, 4)
		timeleft = calcresult - nowdate
		restext = "**__ℹ️NOTICE__**\n引数として**day:**`{}`, **hour:**`{}`, **minute:**`{}`を自動代入しました\n".format(timeleft.days, int(timeleft.seconds / 3600), int(timeleft.seconds / 60 % 60))
	else:
		work = nowdate + datetime.timedelta(days=day, hours=hour, minutes=minute)
		if all([hour == 0, minute == 0]):
			calcresult = datetime.datetime(work.year, work.month, work.day)
			resultfmt = '%m/%d'
		elif minute == 0:
			calcresult = datetime.datetime(work.year, work.month, work.day, work.hour)
			resultfmt = '%m/%d %H:00'
		else:
			calcresult = work
	calcepoc = int(time.mktime(calcresult.timetuple()))

	restext += "```\n{rdate}まで( <t:{repoc}:R> )\n```\n**__Preview__**\n{rdate}まで( <t:{repoc}:R> )".format(rdate = calcresult.strftime(resultfmt), repoc = calcepoc)
	await ctx.respond(restext, ephemeral=True)

	men = await bot.fetch_user(ctx.author.id)
	LOG.debug("{} calculated the date. now:{} + arg:(day:{}, hour:{}, minute:{}) -> {}, epoc:{}".format(men, nowdate.strftime('%m/%d %H:%M'), day, hour, minute, calcresult.strftime(resultfmt), calcepoc))

@bot.event
async def on_command_error(ctx, error):
	LOG.exception("エラーが発生しました")

# 設定ファイルのオープン
with open('settings.json', 'r') as f:
	settings = json.load(f)

# タイトルの設定
titletext = "BP_Dice Version:{} CommitDate:{}".format(settings['Version'], settings['CommitDate'])
title(titletext)

# ログファイル出力先のディレクトリが存在しない場合作成する
if os.path.isdir('log') == False:
	os.mkdir('log')

# ログファイル名の設定
logfilepath = "log/{}.log".format(datetime.date.today().strftime('%Y-%m-%d'))
settings["LoggingConfigulation"]["handlers"]["file"]["filename"] = logfilepath

config.dictConfig(settings["LoggingConfigulation"])
LOG = getLogger(__name__)

LOG.info("*********************************************")
LOG.info(titletext)
LOG.debug("")
LOG.debug("version info:")
LOG.debug("python -> {}".format(platform.python_version()))
LOG.debug("pycord -> {}".format(discord.__version__))
LOG.info("*********************************************")

bot.run(BP_Dice_token.DiscordBotToken)