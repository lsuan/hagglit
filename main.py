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
    
    title = ":bangbang: **WARNING MISSING REQUIRED ARGUMENTS** :bangbang:"
    description = f"{ctx.author.mention} LEA MICHELE! This command takes {len(params)} argument"   
    if len(params) != 1:
      description += "s"
    description += ", but you only gave {0} :cry:\n".format(count)
    description += "***~{0}*** **{1}**".format( command.name, " ".join(params.keys()) )
    color = discord.Color.red()
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1018469333522972692/1019899888873517127/unknown.png")
    embed.set_footer(icon_url=ctx.author.display_avatar, text="Silly Gether")
    await ctx.send(embed=embed)
  else:
    print(error)

@bot.command(description="find out how much slay % you have", extras={"type": "misc"})
async def slaygend(ctx, *member):
  if len(member) > 1:
    await ctx.send(embed=too_many_args_error(ctx.command, member, 1, ctx.author))
  elif member is None or len(member) == 0:
    member = ctx.author
  else:
    member = member[0]
  
  if type(member) is str:
    member_id = int(member[2:-1])
    member = bot.get_user(member_id)
  
  emojis = [
    bot.get_emoji(1018037254712741948),
    bot.get_emoji(1019006925255483554),
    bot.get_emoji(1019007071653478440),
    bot.get_emoji(1020181877350469663),
    bot.get_emoji(1018038550429712434),
    bot.get_emoji(1018036911140515900)
  ]

  await ctx.send(embed=get_slay_percentage(member, emojis))

@bot.command(description="ask a TO1 member a yes/no question", extras={"type": "misc"})
async def menpa(ctx, question):
  await ctx.send(embed=get_answers(ctx.author))

@bot.command(description="get your daily care from a random TO1 member; resets at 12am pst", extras={"type": "care"})
async def greeting(ctx):
  try:
    embed = get_greeting(ctx.author)
    # artist = ARTISTS[ctx.author.name]
    # if artist.get_daily_counter() > 4:
    #   await ctx.send(f"/timeout user:{ctx.author.mention} duration:60 seconds")
  except:
    embed = greeting_error(ctx.author)
  
  await ctx.send(embed=embed)

@bot.command(description="get your care history", extras={"type": "care"})
async def collection(ctx, *member):
  if len(member) > 1:
    await ctx.send(embed=too_many_args_error(ctx.command, member, 1, ctx.author))
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
  embed = help_commands(commands, ctx.author)
  await ctx.send(embed=embed)

bot.run(os.getenv("TOKEN"))