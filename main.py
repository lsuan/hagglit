from cgitb import text
from copy import error
import discord
from discord.ext.commands import Bot
from discord.ext.commands.errors import MissingRequiredArgument, CommandInvokeError
import os
from dotenv import load_dotenv
from management import *
from urllib.parse import urlparse

import Paginator

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
  elif isinstance(error, CommandInvokeError):
    print(str(error))
    if "ConnectionError" in str(error):
      title = ":skull: CONNECTION ERROR :skull:"
      description = "Sorry about that! Try ***~{}*** again".format(ctx.command.name)
      color = discord.Color.red()
      embed = discord.Embed(title=title, description=description, color=color)
      emoji = bot.get_emoji(1020181877350469663)
      embed.set_thumbnail(url=emoji.url)
      embed.set_footer(icon_url=bot.user.display_avatar.url, text="Silly Bot!")
      await ctx.send(embed=embed)
  else:
    print(type(error))
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
    await ctx.send(embed=embed)
    # artist = ARTISTS[ctx.author.name]
    # if artist.get_daily_counter() > 4:
    #   await ctx.send(f"/timeout user:{ctx.author.mention} duration:60 seconds")    
  except Exception as e:
    print("Erere")
    print(e)
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
  role = title + "-" + category
  members = set([ctx.author])

  for gm in guild.members:
    for r in gm.roles:
      if r.name == role:
        members.add(gm)

  is_group = len(members) > 1

  platform_split = platform.split("+")
  platform_emojis = []
  for p in platform_split:
    if p.lower() == "twitter":
      platform_emojis.append("<:twitter:1018066923570860062>")
    elif p.lower() == "tiktok":
      platform_emojis.append("<:tiktok:1018067481669140520>")
    elif p.lower() == "smule":
      platform.emojis.append("<:smule:1019751433651888129>")

  embed = add_project_to_db(title, ctx.author, category, is_group, release_date, platform_emojis, members)
  await ctx.send(embed=embed)

@bot.command(description="change the release date for a project", extras={"type": "project"})
async def edit_project_release(ctx, project_id, release_date):
  try:
    d = datetime.strptime(release_date, "%m/%d/%y")
    project = PROJECTS[project_id]
    project.set_release_date(d)
    update_db(PROJECTS_SHEET, project_id, ["F"], release_date)
    title = ":video_camera: PROJECT UPDATED! :video_camera:"
    description = ":spiral_calendar: {0}'s release date was updated to {1}".format(project.get_title(), project.get_release_date())
    color = discord.Color.random()
    embed = discord.Embed(title=title, description=description, color=color)
    emoji = bot.get_emoji(1020879965257998456)
    embed.set_thumbnail(url=emoji.url)
    embed.set_footer(text=f"Edit made by {ctx.author.mention}", url=ctx.author.display_avatar.url)
  except ValueError:
    title = ":bangbang: INCORRECT DATE FORMAT :bangbang:"
    description = ":spiral_calendar: Make sure your date is in MM/DD/YY format!"
    color = discord.Color.red()
    embed = discord.Embed(title=title, description=description, color=color)
    emoji = bot.get_emoji(1019006925255483554)
    embed.set_thumbnail(url=emoji.url)
    embed.set_footer(text="Silly Gether", icon_url=ctx.author.display_avatar.url)
  except:
    title = "SOMETHING WENT WRONG! :cry:"
    color = discord.Color.red()
    description = f"{ctx.author.mention}, try **~edit_project** again! :pray:"
    embed = discord.Embed(title=title, description=description, color=color)
    emoji = bot.get_emoji(1020181877350469663)
    embed.set_thumbnail(url=emoji.url)
    embed.set_footer(icon_url=bot.user.display_avatar.url, text="Silly Bot!")

@bot.command(description="get all the projects", extras={"type": "project"})
async def projects(ctx):
  pages = get_projects()
  previous = discord.ui.Button(label="Back", style=discord.ButtonStyle.blurple)
  next = discord.ui.Button(label="Next", style=discord.ButtonStyle.blurple)
  page_counter_style = discord.ButtonStyle.grey
  initial = 0
  timeout = 500
  await Paginator.Simple(PreviousButton=previous, NextButton=next, PageCounterStyle=page_counter_style, InitialPage=initial, timeout=timeout).start(ctx, pages)
  # await ctx.send(embed=embed)

@bot.command(description="gets the social media analytics of a project", extras={"type": "project"})
async def get_project_stats(ctx, id, url):
  project = PROJECTS[int(id)]
  hostname = urlparse(url).hostname
  hostname_split = hostname.split(".")

  if "twitter" in hostname_split:
    platform = "twitter"
    platform_emoji = "<:twitter:1018066923570860062>"
  elif "tiktok" in hostname_split:
    platform = "tiktok"
    platform_emoji = "<:tiktok:1018067481669140520>"
  elif "smule" in hostname_split:
    platform = "smule"
    platform_emoji = "<:smule:1019751433651888129>"
  
  embed = get_project_analytics(ctx.author, project, platform, platform_emoji, url)
  await ctx.send(embed=embed)

@bot.command(extras={"type": "help"})
async def help(ctx):
  commands = sorted(bot.commands, key=lambda c: c.name)
  embed = help_commands(commands, ctx.author)
  await ctx.send(embed=embed)
 
bot.run(os.getenv("TOKEN"))