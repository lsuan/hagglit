from dis import disco
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
  guild = bot.get_guild(guild_id)
  initialize_artists(guild)
  initialize_to1()

@bot.event
async def on_message(message):
  user = message.author

  if user == bot.user:
    return
  
  if message.content.startswith("~greeting"):
    embed = greeting(user)
    await message.channel.send(embed=embed)
    # await message.channel.send(greeting(user))
  if message.content.startswith("~collection"):
    args = message.content.split(" ")[1:]
    if len(args) == 0:
      target = user
    elif len(args) > 1:
      await message.channel.send("Too many arguments! Send only one user or none!")
      return
    else:
      target = args[0]

    await message.channel.send(get_collection(user))

bot.run(os.getenv("TOKEN"))
