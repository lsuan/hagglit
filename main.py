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

@bot.command()
async def slaygend(ctx, member = None):
  if member is None:
    member = ctx.author

  await ctx.send(get_slay_percentage(member))

@bot.command()
async def greeting(ctx):
  try:
    embed=get_greeting(ctx.author)
  except:
    embed=greeting_error(ctx.author)
  
  await ctx.send(embed=embed)

@bot.command()
async def collection(ctx, member = None):
  if member is None:
    member = ctx.author
  await ctx.send(embed=get_collection(member))

bot.run(os.getenv("TOKEN"))

@bot.command()
async def add_project(ctx, project_name, is_group, release_date, platform):
  pass

@bot.command()
async def projects(ctx):
  pass