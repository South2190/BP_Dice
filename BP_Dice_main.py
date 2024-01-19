import discord
import random

import BP_Dice_resource

bot = discord.Bot()

@bot.slash_command(guild_ids=[BP_Dice_resource.ServerID])
async def dice(ctx):
	await ctx.respond('ダイス！【{}】'.format(random.randint(0, 999)))

bot.run(BP_Dice_resource.DiscordBotToken)