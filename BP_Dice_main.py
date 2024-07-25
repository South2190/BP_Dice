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

# サーバー設定ファイル
ServerSettingsFile = 'server-settings.json'
# Bot設定ファイル
BotSettingsFile = 'settings.json'
# サーバーIDをログに出力する際のフォーマット
GuildInfoDump = lambda gid: f"(GuildID:{gid}) "

ChannelList = []
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents = intents)

# 削除ボタン実装の試み
"""
class AutoCpcalcOption(discord.ui.View):
	@discord.ui.button(style = discord.ButtonStyle.grey, emoji = "🗑️")
	async def MessageDelete(self, button, interaction):
		await interaction.delete_original_response()
"""

# ウインドウタイトルの設定
def title(text):
    # Windows
	if os.name == 'nt':
		os.system(f'title {text}')
    # Mac / Linux
	elif os.name == 'posix':
		print(f'\x1b]2;{text}\x07', end = '', flush = True)

# 発言の監視対象チャンネルのリストを更新
def ChannelListReload():
	global ChannelList
	ChannelList = []
	for item in ServerSettings["GuildIds"].values():
		ChannelList.append(item["CouponcodeChannel"])

# Bot起動時の処理
@bot.event
async def on_ready():
	await bot.change_presence(activity = discord.Game(name = "/help"))
	LOG.info("Botの起動が完了しました")

# コマンドでエラーが発生した場合の処理
@bot.event
async def on_application_command_error(ctx, error):
	# LOG.exceptionがエラーとして認識していない？感じなので無理やり例外を発生させて内容をログファイルに記録する
	try:
		raise error
	except:
		LOG.exception("エラーが発生しました")

# コネクトクーポンの有効期限の自動返信処理
@bot.event
async def on_message(message: discord.Message):
	# Botからのメッセージは無視
	if message.author.bot:
		return
	# メッセージが2行以上の場合は無視
	if '\n' in message.content:
		return
	# 設定されたチャンネル以外で送信されたメッセージの場合は無視
	if message.channel.id not in ChannelList:
		return
	# テスター以外のメッセージは無視
	if message.author.id not in TesterUserList:
		return

	resultfmt = '%m/%d %H:%M'
	nowdate = datetime.datetime.now()
	work = nowdate + datetime.timedelta(days = 31) if nowdate.hour >= 4 else nowdate + datetime.timedelta(days = 30)
	calcresult = datetime.datetime(work.year, work.month, work.day, 4)
	# エポック秒の算出
	calcepoc = int(time.mktime(calcresult.timetuple()))
	#await message.reply("{rdate}まで( <t:{repoc}:R> )".format(rdate = calcresult.strftime(resultfmt), repoc = calcepoc), view = AutoCpcalcOption(), mention_author = False, silent = True)
	await message.reply("{rdate}まで( <t:{repoc}:R> )".format(rdate = calcresult.strftime(resultfmt), repoc = calcepoc), mention_author = False, silent = True)
	LOG.debug(GuildInfoDump(message.guild.id) + "now:{} -> {}, epoc:{}".format(nowdate.strftime('%m/%d %H:%M'), calcresult.strftime('%m/%d %H:%M'), calcepoc))

# helpコマンドの定義
@bot.slash_command(description = "コマンドの使用方法を表示します")
async def help(
	ctx: discord.ApplicationContext,
	command: Option(str, description = "コマンド名", choices = ["list", "help", "dice", "cpcalc"], required = False, default = "list"),
	ephemeral: Option(bool, description = "実行結果を他人から見えないようにする（既定値：True）", required = False, default = True)
):
	# settings.jsonに記述しているヘルプの文章を読み込む
	helptext = Settings["HelpFormat"][command]
	embed = discord.Embed(
		#title = helptext["title"],
		description = helptext["description"],
		color = 0x3c88da
	)
	embed.set_image(url = helptext["set_image"])
	for d in helptext["add_field"]:
		embed.add_field(name = d, value = helptext["add_field"][d])

	await ctx.respond(embed = embed, ephemeral = ephemeral)
	LOG.debug(GuildInfoDump(ctx.guild_id) + "command:{}, ephemeral:{}".format(command, ephemeral))

# diceコマンドの定義
@bot.slash_command(description = "ダイスを振ります（範囲：0～999）")
async def dice(ctx):
	dicenum = random.randint(0, 999)
	await ctx.respond("ダイス！【{}】".format(dicenum))
	LOG.debug(GuildInfoDump(ctx.guild_id) + "{}".format(dicenum))

# cpcalcコマンドの定義
@bot.slash_command(description = "コネクトクーポンの有効期限の日付を計算します")
async def cpcalc(
	ctx: discord.ApplicationContext,
	couponcode: Option(str, description = "クーポンコード", required = False, default = None),
	day: Option(int, description = "残り日数", required = False, default = 0),
	hour: Option(int, description = "残り時間数", required = False, default = 0),
	minute: Option(int, description = "残り分数", required = False, default = 0)
):
	gentext = ""
	restext = ""
	auto = ""
	nowdate = datetime.datetime.now()
	resultfmt = '%m/%d %H:%M'

	# 引数の指定が無い場合は自動的に30日後の翌4時で計算する
	if all([day == 0, hour == 0, minute == 0]):
		if nowdate.hour == 4 and nowdate.minute <= 30:
			restext = "⚠️ゲーム内ログインボーナス更新直後にコマンドが実行されています。下記の残り有効期限が正しいかどうか確認してください。\n"
		work = nowdate + datetime.timedelta(days = 31) if nowdate.hour >= 4 else nowdate + datetime.timedelta(days = 30)
		calcresult = datetime.datetime(work.year, work.month, work.day, 4)
		# 差分の計算
		timeleft = calcresult - nowdate
		h = int(timeleft.seconds / 3600)
		m = int(timeleft.seconds / 60 % 60)
		restext += "ℹ️有効期限　残り：`{}`日`{}`時間`{}`分として自動で計算しました。\n".format(timeleft.days, h, m)
		auto = " auto:(day:{}, hour:{}, minute:{})".format(timeleft.days, h, m)
	# 引数が指定された場合
	else:
		work = nowdate + datetime.timedelta(days = day, hours = hour, minutes = minute)
		if all([hour == 0, minute == 0]):
			calcresult = datetime.datetime(work.year, work.month, work.day)
			resultfmt = '%m/%d'
		elif minute == 0:
			calcresult = datetime.datetime(work.year, work.month, work.day, work.hour)
			resultfmt = '%m/%d %H:00'
		else:
			calcresult = work

	# エポック秒の算出
	calcepoc = int(time.mktime(calcresult.timetuple()))

	# 生成テキスト設定
	if couponcode != None:
		gentext = couponcode + "\n"
	gentext += "{rdate}まで( <t:{repoc}:R> )".format(rdate = calcresult.strftime(resultfmt), repoc = calcepoc)

	# 返信の書式設定
	restext += "```\n{gentext}\n```\n**__Preview__**\n{gentext}".format(gentext = gentext)

	# 送信
	await ctx.respond(restext, ephemeral = True)
	# ログへの出力
	LOG.debug(GuildInfoDump(ctx.guild_id) + "now:{} + arg:(day:{}, hour:{}, minute:{}){} -> {}, epoc:{}".format(nowdate.strftime('%m/%d %H:%M'), day, hour, minute, auto, calcresult.strftime(resultfmt), calcepoc))

# コネクトクーポンの有効期限の自動返信先チャンネル設定(サーバー管理者のみ実行可能)
@bot.slash_command(description = "コネクトクーポンの有効期限の自動返信先チャンネルを指定します", default_member_permissions = discord.permissions.Permissions(manage_guild = True))
@discord.guild_only()
async def set_cpcalc_channel(
	ctx: discord.ApplicationContext,
	ch: Option(discord.abc.GuildChannel, description = "チャンネル"),
):
	await ctx.respond("コネクトクーポンの有効期限をチャンネル <#{}> に自動で返信するよう設定しました".format(ch.id))
	# コマンドを実行したサーバーの設定が存在しない場合辞書を定義
	if str(ctx.guild_id) not in ServerSettings["GuildIds"]:
		ServerSettings["GuildIds"][str(ctx.guild_id)] = {}
		ServerSettings["GuildIds"][str(ctx.guild_id)]["GuildName"] = f"{ctx.guild}"
	ServerSettings["GuildIds"][str(ctx.guild_id)]["CouponcodeChannel"] = ch.id
	# サーバー設定ファイルへの書き込み
	with open(ServerSettingsFile, 'w', encoding = "utf-8") as f:
		json.dump(ServerSettings, f, indent = 4, ensure_ascii = False)
	ChannelListReload()
	LOG.debug(GuildInfoDump(ctx.guild_id) + "ch.id:{}".format(ch.id))

# 起動準備
# Bot設定ファイルのオープン
with open(BotSettingsFile, 'r', encoding = "utf-8") as f:
	Settings = json.load(f)

# サーバー設定ファイルのオープン
if (os.path.isfile(ServerSettingsFile)):
	with open(ServerSettingsFile, 'r', encoding = "utf-8") as f:
		ServerSettings = json.load(f)
	ChannelListReload()
else:
	# サーバー設定ファイルが存在しない場合辞書を定義
	ServerSettings = {}
	ServerSettings["GuildIds"] = {}

# コネクポ有効期限自動返信機能のテスターリスト読み込み
with open("TesterUserList.json", 'r', encoding = "utf-8") as f:
	TesterUserList = json.load(f)

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