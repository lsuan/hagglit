import discord
from random import randint
from datetime import date

from artist import Artist
from to1member import TO1Member

ARTISTS = {}
TO1_MEMBERS = {}

def initialize_to1():
  TO1_MEMBERS["Donggeon"] = TO1Member("Donggeon", ":lion_face:", "#d42040", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469434874134549/Donggeon.jpeg")
  TO1_MEMBERS["Jisu"] = TO1Member("Jisu", ":turtle:", "#d5bc2d", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469435331317830/Jisu.jpeg")
  TO1_MEMBERS["Jaeyun"] = TO1Member("Jaeyun", ":teddy_bear:", "#d63b3a", "https://media.discordapp.net/attachments/1018469333522972692/1018469435121606747/Jaeyun.jpeg")
  TO1_MEMBERS["J.You"] = TO1Member("J.You", ":dragon:", "#987c8b", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469435603959928/JYou.jpeg")
  TO1_MEMBERS["Kyungho"] = TO1Member("Kyungho", ":black_cat:", "#5a995c", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469435851415572/Kyungho.jpeg")
  TO1_MEMBERS["Daigo"] = TO1Member("Daigo", ":flame:", "#e88367", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469434572156958/Daigo.jpeg")
  TO1_MEMBERS["Renta"] = TO1Member("Renta", ":smiling_imp:", "#e72339", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469436111466586/Renta.jpeg")
  TO1_MEMBERS["Yeojeong"] = TO1Member("Yeojeong", ":man_fairy:", "#e9975b", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469436421853194/Yeojeong.jpeg")

def initialize_artists(guild):
  for gm in guild.members:
    if not gm.bot:
      ARTISTS[gm] = Artist(gm)

def greeting(user):
  index = randint(0, len(TO1_MEMBERS.keys())-1)
  member = list(TO1_MEMBERS.keys())[index]
  ARTISTS[user].add_daily( member, date.today() )

  title = ":sparkling_heart: TO: {0} :sparkling_heart:".format(user.display_name)
  # title = " GREETINGS FROM {0} {1} :sparkling_heart:".format(member.upper(), TO1_MEMBERS[member].get_emoji())
  description = "{0}아 안녕~\n오늘도 beautiful day 하겠다 ^^ 사랑해 :hand_with_index_finger_and_thumb_crossed:\n".format(user.display_name)
  description += "**FROM: {0}** {1}".format(member, TO1_MEMBERS[member].get_emoji())

  embed = discord.Embed()
  embed.title = title
  embed.description = description
  embed.color = discord.Color.from_str(TO1_MEMBERS[member].get_embed_color())
  embed.set_image(url= TO1_MEMBERS[member].get_image())
  return embed

  # greeting = \
  #   ":sparkling_heart: {0} :sparkling_heart:\n".format(user.display_name) + \
  #   "{0} {1} says hi~ hehe\n".format(member, TO1_MEMBERS[member]) + \
  #   "\"{0}아 안녕~ 오늘도 beautiful day 하겠다 ^^ 사랑해 :hand_with_index_finger_and_thumb_crossed:\"".format(user.display_name)

def get_collection(user):
  artist = ARTISTS[user]
  collection = artist.get_daily_collection()
  member_counts = {}
  first_care, last_care = None, None

  if len(collection) == 0:
    return ""

  # collection: [ () ]
  for member in collection:
    if member[0] in member_counts:
      member_counts[member[0]] += 1
      if member[1] > last_care:
        last_care = member[1]
    else:
      member_counts[member[0]] = 1
      first_care = member[1]
      last_care = member[1]

  print(member_counts)
  result = \
    "{0} has gotten :sparkling_heart: care :sparkling_heart: from\n".format(artist.stage_name)
  
  sorted_members = sorted(member_counts.items(), key=lambda item: -item[1])
  most_loving_member = sorted_members[0][0]
  
  first_care_format = first_care.strftime("%m/%d/%y")
  if last_care:
    last_care_format = last_care.strftime("%m/%d/%y")

  for member, count in sorted_members:
    result += "\t:heartpulse: {0} {1} {2} times! First care: {3}".format(member, TO1_MEMBERS[member].get_emoji(), count, first_care_format)
    if last_care:
      result += " | Latest care: {0}".format(last_care_format)
    result += "\n"
  
  total_cares = sum(list(member_counts.values()))

  if len(sorted_members) > 3 and total_cares > 5:
    result += "hehe {0} {1} care you so much :pleading_face:".format(most_loving_member, TO1_MEMBERS[most_loving_member].get_emoji())
  
  return result