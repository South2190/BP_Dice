import discord
import BP_Dice_resource

bot = discord.Bot()

@bot.slash_command(guild_ids=[889855802054156288])
async def aping(ctx):
	print("catch aping")
	await ctx.respond('apong')

bot.run(BP_Dice_resource.DiscordBotToken)