import discord
import os
from management import *

intents = discord.Intents.default()
client = discord.Client(intents=intents)
prefix = "~"


@client.event
async def on_ready():
  print("{0.user} is ready to slay!".format(client))


@client.event
async def on_message(message):
  if not message.content.startwith(prefix) or message.author == client.user:
    return

  args = message.content[1:].split(" ")
  command = args[1]

  if command == "greeting":
    await message.channel.send(greeting())

print(os.getenv("TOKEN"))

# client.run(os.getenv("TOKEN"))
