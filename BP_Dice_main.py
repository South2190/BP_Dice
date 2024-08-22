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

# Bot設定ファイル
BotSettingsFile = 'settings.json'
# サーバーIDをログに出力する際のフォーマット
GuildInfoDump = lambda gid: f"(GuildID:{gid}) "

ChannelList = []
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents = intents)

# コマンド呼び出しボタン
class CallCommandButton(discord.ui.View):
	@discord.ui.button(label = "有効期限を計算する", style = discord.ButtonStyle.blurple, emoji = "🎫")
	async def CpcalcButton(self, button, interaction):
		await interaction.response.send_modal(CouponCodeModal(title = "クーポンコードを入力"))

# クーポンコードの入力を求めるモーダル
class CouponCodeModal(discord.ui.Modal):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.add_item(discord.ui.InputText(label = "クーポンコード", style = discord.InputTextStyle.short))

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.send_message(self.children[0].value, ephemeral = True)

# ウインドウタイトルの設定
def title(text):
    # Windows
	if os.name == 'nt':
		os.system(f'title {text}')
    # Mac / Linux
	elif os.name == 'posix':
		print(f'\x1b]2;{text}\x07', end = '', flush = True)

# コネクトクーポンの有効期限を計算
def CpAutoCalc(cpcode, day, hour, minute):
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
	if cpcode != None:
		#gentext = cpcode + "\n"
		gentext = f"```\n{cpcode}\n```\n"
	gentext += "{rdate}まで( <t:{repoc}:R> )".format(rdate = calcresult.strftime(resultfmt), repoc = calcepoc)
	# 返信の書式設定
	restext += "````\n{gentext}\n````\n**__Preview__**\n{gentext}".format(gentext = gentext)

	# ログへの出力
	LOG.debug("now:{} + arg:(day:{}, hour:{}, minute:{}){} -> {}, epoc:{}".format(nowdate.strftime('%m/%d %H:%M'), day, hour, minute, auto, calcresult.strftime(resultfmt), calcepoc))

	return restext

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

# command_buttonコマンドの定義
@bot.slash_command(description = "コマンド呼び出しボタンを備えたメッセージを送信します", default_member_permissions = discord.permissions.Permissions(manage_guild = True))
@discord.guild_only()
async def command_button(ctx):
	await ctx.respond("test", view = CallCommandButton())

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
	LOG.debug("CpAutoCalcを呼び出します")
	text = CpAutoCalc(couponcode, day, hour, minute)
	# 送信
	await ctx.respond(text, ephemeral = True)

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