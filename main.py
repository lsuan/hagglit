from datetime import timedelta
import discord
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv
from management import *

load_dotenv()
intents = discord.Intents.all()
bot = Bot(command_prefix="~", intents=intents)
guild_id = int(os.getenv("GUILD_ID"))

@bot.event
async def on_ready():
  print("{0.user} is ready to slay!".format(bot))
  # guild = bot.get_guild(guild_id)
  # channel = bot.get_channel(1018406561770639451)
  # await channel.send("{0.user} is ready to slay!".format(bot))

@bot.command()
async def slaygend(ctx, member = None):
  if member is None:
    member = ctx.author

  await ctx.send(get_slay_percentage(member))

@bot.command()
async def greeting(ctx):
  await ctx.send(embed=get_greeting(ctx.author))

@bot.command()
async def collection(ctx, member = None):
  if member is None:
    member = ctx.author
  await ctx.send(embed=get_collection(member))

bot.run(os.getenv("TOKEN"))
