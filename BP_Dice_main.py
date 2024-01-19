import discord

bot = discord.Bot()

@bot.slash_command(guild_ids=[889855802054156288])
async def aping(ctx):
	print("catch aping")
	await ctx.respond('apong')

bot.run('ODg5ODU3NDE3MjAwOTM0OTEz.GoxEVi.ChmCCDUCiFKNsw-ZQPtOMq9Kp5K9X0pfSPZ33c')