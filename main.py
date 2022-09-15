import discord
from discord.ext.commands import Bot
from discord.ext.commands.errors import MissingRequiredArgument
import os
from dotenv import load_dotenv
from management import *

load_dotenv()
intents = discord.Intents.all()
bot = Bot(command_prefix="~", intents=intents)
bot.remove_command("help")
guild_id = int(os.getenv("GUILD_ID"))

@bot.event
async def on_ready():
  print("{0.user} is ready to slay!".format(bot))

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, MissingRequiredArgument):
    command = ctx.command
    params = command.clean_params
    count = 0
    missing_param = str(error).split()[0]
    for param in params:
      if param == missing_param:
        break
      count += 1
    title = ":bangbang: **WARGING MISSING REQUIRED ARGUMENTS** :bangbang:"
    description = f"{ctx.author.mention} LEA MICHELE! This command takes {len(params)} arguments, but you only gave {count} :cry:\n"
    description += "***~{0}*** **{1}**".format( command.name, " ".join(params.keys()) )
    color = discord.Color.red()
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1018469333522972692/1019899888873517127/unknown.png")
    embed.set_footer(icon_url=ctx.author.display_avatar, text="Silly Gether")
    await ctx.send(embed=embed)
  else:
    print(error)

@bot.command(description="find out how much slay % you have", extras={"type": "misc"})
async def slaygend(ctx, member = None):
  if member is None:
    member = ctx.author

  await ctx.send(get_slay_percentage(member))

@bot.command(description="get your daily care from a random TO1 member; resets at 12am pst", extras={"type": "care"})
async def greeting(ctx):
  try:
    embed = get_greeting(ctx.author)
    artist = ARTISTS[ctx.author.name]
    if artist.get_daily_counter() > 4:
      await ctx.send(f"/timeout user:{ctx.author.mention} duration:60 seconds")
  except:
    embed = greeting_error(ctx.author)
  
  await ctx.send(embed=embed)

@bot.command(description="get your care history", extras={"type": "care"})
async def collection(ctx, *member):
  if len(member) > 1:
    title = ":bangbang: **WARNING TOO MANY ARGUMENTS** :bangbang:"
    description = f"{ctx.author.mention} LEA MICHELE! This command takes {0} argument, but you gave {1} :rage:\n".format(1, len(member))
    description += "***~collection*** *@user*"
    color = discord.Color.random()
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1018469333522972692/1019899888873517127/unknown.png")
    embed.set_footer(icon_url=ctx.author.display_avatar, text="Silly Gether :rolling_eyes:")
    await ctx.send(embed=embed)
  elif member is None or len(member) == 0:
    member = ctx.author
  else:
    member = member[0]
  
  if type(member) is str:
    member_id = int(member[2:-1])
    member = bot.get_user(member_id)

  try:
    await ctx.send(embed=get_collection(member))
  except:
    await ctx.send(embed=get_collection(member))

@bot.command(description="add a project to be released on social media", extras={"type": "project"})
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

  platform_split = platform.split("+")
  platform_emojis = []
  for p in platform_split:
    if p.lower() == "twitter":
      platform_emojis.append("<:twt:1018066923570860062>")
    elif p.lower() == "tiktok":
      platform_emojis.append("<:tiktok:1018067481669140520>")
    elif p.lower() == "smule":
      platform.emojis.append("<:smule:1019751433651888129>")

  is_group = len(members) > 1
  embed = add_project_to_db(title, ctx.author, category, is_group, release_date, platform_emojis, members)
  await ctx.send(embed=embed)

@bot.command(description="get all the projects", extras={"type": "project"})
async def projects(ctx):
  embed = get_projects()
  await ctx.send(embed=embed)

@bot.command(extras={"type": "help"})
async def help(ctx):
  commands = sorted(bot.commands, key=lambda c: c.name)
  care_commands = list(filter(lambda c: c.extras["type"] == "care", commands))
  project_commands = list(filter(lambda c: c.extras["type"] == "project", commands))
  misc_commands = list(filter(lambda c: c.extras["type"] == "misc", commands))

  title = ":exclamation: ALL COMMANDS :exclamation:"
  description = "**BOLDED PARAMS** = **REQUIRED**\n*ITALICIZED PARAMS* = *OPTIONAL*"
  color = discord.Color.random()
  embed = discord.Embed(title=title, description=description, color=color)
  embed.add_field(name=("—+" * 10)[:-1], value="\u200B", inline=False)
  
  if len(care_commands) > 0:
    care_title = ":sparkling_heart: CARE COMMANDS :sparkling_heart:"
    make_embed_commands_col(embed, care_title, "", care_commands)
  embed.add_field(name=("—+" * 10)[:-1], value="\u200B", inline=False)
  
  if len(project_commands) > 0:
    project_title = ":video_camera: PROJECT COMMANDS :video_camera:"
    make_embed_commands_col(embed, project_title, "", project_commands)
  embed.add_field(name=("—+" * 10)[:-1], value="\u200B", inline=False)

  if len(misc_commands) > 0:
    misc_title = ":partying_face: MISCELLANEOUS COMMANDS: :partying_face:"
    make_embed_commands_col(embed, misc_title, "", misc_commands)

  text = f"Requested by {ctx.author.display_name}"
  embed.set_footer(icon_url=ctx.author.display_avatar, text=text)
  await ctx.send(embed=embed)

def make_embed_commands_col(embed, name, value, commands):
  for command in commands:
    parameters = command.clean_params.values()
    required = ["**"+ cp.name + "**" for cp in parameters if cp.required]
    optional = ["*"+ cp.name + "*" for cp in parameters if not cp.required]
    parameters = required + optional
    value += ":pushpin: __***~{0}***__ {1}\n".format(command.name, " ".join(parameters))
    value += ":pencil: {0}\n".format(command.description)
  embed.add_field(name=name, value=value)

bot.run(os.getenv("TOKEN"))