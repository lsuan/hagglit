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
  if type(member) is str:
    member_id = int(member[2:-1])
    member = bot.get_user(member_id)

  try:
    await ctx.send(embed=get_collection(member))
  except:
    await ctx.send(embed=get_collection(member))

@bot.command()
async def add_project(ctx, title, category, release_date, platform):
  guild = bot.get_guild(guild_id)
  roles =  guild.roles
  role = filter(lambda r: r.name.endswith(category), roles)
  for r in role:
    break

  members_roles = defaultdict(set)
  for gm in guild.members:
    for role in gm.roles:
      members_roles[role.name].add(gm)
  members = members_roles[r.name]

  if platform.lower() == "twitter":
    emoji = "<:twt:1018066923570860062>"
  elif platform.lower() == "tiktok":
    emoji = "<:tiktok:1018067481669140520>"

  is_group = len(members) > 1
  embed = add_project_to_db(title, ctx.author, category, is_group, release_date, emoji, members)
  await ctx.send(embed=embed)

@bot.command()
async def projects(ctx):
  embed = get_projects()
  await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))