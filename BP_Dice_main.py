import datetime
import discord
import json
import os
import platform
import random
from logging import getLogger, config

import BP_Dice_token

# Bot設定ファイル
BotSettingsFile = 'settings.json'
# サーバーIDをログに出力する際のフォーマット
GuildInfoDump = lambda gid: f"(GuildID:{gid}) "

bot = discord.Bot()

# ウインドウタイトルの設定
def title(text):
    # Windows
	if os.name == 'nt':
		os.system(f'title {text}')
    # Mac / Linux
	elif os.name == 'posix':
		print(f'\x1b]2;{text}\x07', end = '', flush = True)

# Bot起動時の処理
@bot.event
async def on_ready():
	await bot.change_presence(activity = discord.Game(name = "BLUE PROTOCOL"))
	LOG.info("Botの起動が完了しました")

# コマンドでエラーが発生した場合の処理
@bot.event
async def on_application_command_error(ctx, error):
	# LOG.exceptionがエラーとして認識していない？感じなので無理やり例外を発生させて内容をログファイルに記録する
	try:
		raise error
	except:
		LOG.exception("エラーが発生しました")

# diceコマンドの定義
@bot.slash_command(description = "ダイスを振ります（範囲：0～999）")
async def dice(
	ctx: discord.ApplicationContext,
	upperlimit: discord.Option(int, description = "最大値", required = False, default = 0),
	ephemeral: discord.Option(bool, description = "実行結果を他人から見えないようにする（True->有効、False->無効、既定値：False）", required = False, default = False)
):
	ul = upperlimit if 0 < upperlimit < 1000 else 999
	result = random.randint(0, ul)
	await ctx.respond(f"ダイス！【{result}】", ephemeral = ephemeral)
	LOG.debug(GuildInfoDump(ctx.guild_id) + f"result:{result:<3} ul:{ul:<3} upperlimit:{upperlimit}")

# 起動準備
# Bot設定ファイルのオープン
with open(BotSettingsFile, 'r', encoding = "utf-8") as f:
	Settings = json.load(f)

# タイトルの設定
titletext = "BP_Dice Version:{} CommitDate:{}".format(Settings['Version'], Settings['CommitDate'])
title(titletext)

# ログファイル出力先のディレクトリが存在しない場合作成する
if os.path.isdir('log') == False:
	os.mkdir('log')

# ログファイル名の設定
logfilepath = "log/{}.log".format(datetime.date.today().strftime('%Y-%m-%d'))
Settings["LoggingConfigulation"]["handlers"]["file"]["filename"] = logfilepath

config.dictConfig(Settings["LoggingConfigulation"])
LOG = getLogger(__name__)

LOG.info("*********************************************")
LOG.info(titletext)
LOG.debug("")
LOG.debug("version info:")
LOG.debug("python -> {}".format(platform.python_version()))
LOG.debug("pycord -> {}".format(discord.__version__))
LOG.info("*********************************************")

bot.run(BP_Dice_token.DiscordBotToken)