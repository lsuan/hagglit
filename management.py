from xml.dom import UserDataHandler
import discord
from random import randint

from helpers import *

def get_slay_percentage(user):
  percentage = randint(0, 100)
  message = "{0} :sparkles: SLAY :sparkles: percentage is {1}%".format(user.display_name, randint(0, 100))

  # TODO: FIND OUT HOW TO GET SERVER EMOJIS TO WORK 
  # if percentage < 25:
  #   message += " :emoji_5:"
  # elif percentage < 50:
  #   message += " :emoji_8:"
  # elif percentage < 75:
  #   message += " :emoji_4:"
  # elif percentage < 100:
  #   message += " :emoji_9:"
  # elif percentage == 100:
  #   message += " :gether:"
  
  return message

def get_greeting(user):
  global COLLECTIONS_INDEX
  index = randint(0, len(TO1_MEMBERS.keys())-1)
  member = list(TO1_MEMBERS.keys())[index]
  artist = ARTISTS[user.name]

  ldl = artist.get_last_daily_log()
  if ldl != "" and is_new_day(ldl):
    artist.set_daily_counter(0)

  artist_id = artist.get_id()

  artist.add_daily_counter()
  update_db(ARTISTS_SHEET, artist_id, 4, artist.get_daily_counter())

  responses = [
    "HEY STOP THAT! :rage:",
    "STOP BEING LEA MICHELE! :rage:",
    "KEEP GOING WOULD YA? :rolling_eyes:",
    "SOMEONE'S EXCITED :rolling_eyes:"
  ]
  
  counter = artist.get_daily_counter()
  if counter > 1:
    title = ":bangbang: WARNING {0}:bangbang:".format(counter-1)
    color = discord.Color.random()
    if counter == 2:
      description = "You have already used your daily today!"
    elif counter > 2 and artist.get_daily_counter() < 4:
      description = responses[randint(0, len(responses)-1)]
    elif counter == 4:
      description = "DO IT AGAIN AND YOU'RE GETTING TIMED OUT #/REAL :rage:"
    elif counter == 5:
      description = "jk idk how to do that yet LOL but still stop spamming"
      # description = ":grin:" 
    elif counter >= 6:
      description = "DID THE TIMEOUT WORK?"

    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1018469333522972692/1019899888873517127/unknown.png")
    embed.set_footer(icon_url=user.display_avatar, text="Silly Gether")
    
    return embed
    
  artist.add_daily( member, date.today() )
  artist.set_last_daily_log( date.today() )
  today = date.today().strftime("%m/%d/%y")
  
  update_db(ARTISTS_SHEET, artist_id, 5, today)
  batch_update(COLLECTIONS_SHEET, COLLECTIONS_INDEX, ["A", "B", "C"], [float(artist_id), member, today])
  COLLECTIONS_INDEX += 1

  title = ":sparkling_heart: TO: {0} :sparkling_heart:".format(artist.stage_name)
  description = "{0}아 안녕~\n".format(artist.get_stage_name())
  special_message = _get_special_message(artist, member)
  if special_message == "":
    description += "오늘도 beautiful day 하겠다 ^^ 사랑해 :smiling_face_with_3_hearts:\n"
  else:
    description += special_message

  description += "**FROM: {0}** {1}".format(member, TO1_MEMBERS[member].get_emoji())
  color = discord.Color.from_str(TO1_MEMBERS[member].get_embed_color())
  embed = discord.Embed(title=title, description=description, color=color)
  embed.set_image(url= TO1_MEMBERS[member].get_image())
  return embed

  # greeting = \
  #   ":sparkling_heart: {0} :sparkling_heart:\n".format(user.display_name) + \
  #   "{0} {1} says hi~ hehe\n".format(member, TO1_MEMBERS[member]) + \
  #   "\"{0}아 안녕~ 오늘도 beautiful day 하겠다 ^^ 사랑해 :hand_with_index_finger_and_thumb_crossed:\"".format(user.display_name)

def _get_special_message(artist, to1_member):
  special_messages = {
    "2.3440408228921344e+17": { "Donggeon": "Wow I noticed your SURF outfit at KCON 2022 LA :thumbsup: :heart:" },
    "3.5477441436739174e+17": { "Jaeyun" : "I care and love you the most hehe :heart_hands: :blush:", 
                            "Kyungho": "FINALLY IT'S MY TURN TO LOVE YOU :sunglasses: :heart:" },
    "4.0123820780866765e+17": { "Renta": "Renta care you belly belly much Tate :smiling_face_with_3_hearts:" },
    "4.5629085799848346e+17": { "Renta": "Hana, あなたはとても優しいです、私の一番のファンです。:blush:" },
    "5.89912841868542e+17": { "Yeojeong": "You're my favorite fan hehe :: :blush:",
                            "Jaeyun": "You left me for Yeojeong :sob: but I still love you hehe :heart:" },
    "5.929838293298708e+17": { "Renta": "RENTAPURR :kissing_cat: :heart:",
                            "Kyungho": "Why didn't you let Lee claim me? :cry:" },
    "5.950413077731082e+17": { "Kyungho": "KATY + KYUNGHO = BESTIES FOR LIFE :heart_eyes: :heart:",
                            "Jaeyun": "You're a better leader than me :sweat_smile: :heart:" },
    "6.450977777806213e+17": { "Jisu": "My mom approves of us Zay hehe :heart:" },
    "6.724588262716867e+17": { "Jaeyun": "GB, you are my sweetest fan. :blush: :heart:",
                            "Donggeon": "GB, look at me, not Jaeyun :pleading_face:" },
    "7.563481512076902e+17": { "Jaeyun": "Sorry I made Lee pergant but I still love you (cheater jk) :heart:",
                            "Daigo": "Daigi loves my 딸기잼 :heart:",
                            "Kyungho" : "Stop calling me KERB :cry: :weary:" },
    "9.947420992389777e+17": { "J.You": "I'll look out for you next time I'm in SF :heart:"}
  }

  message = ""
  artist_id = artist.get_id()
  if to1_member in special_messages[artist_id]:
    message = special_messages[artist_id][to1_member] + "\n"
  return message

def greeting_error(user):
  title = "SOMETHING WENT WRONG! :cry:"
  color = discord.Color.red()
  artist = ARTISTS[user.name]
  # mention user in description
  description = f"{user.mention}, try **~greeting** again! :pray:"

  # check first if collections table was updated
  # if it was, don't clear data
  collection = artist.get_daily_collection()
  if collection != [] and collection[-1][1] == date.today():
    description = f"{user.mention}, the record was saved! Try **~collection** to see it! :pray:"
  else:
    aid = str(artist.get_id())
    sheet_values = ARTISTS_SHEET.get_values(value_render_option="UNFORMATTED_VALUE")
    artist_row = get_record_row(sheet_values, aid)
    batch_update(ARTISTS_SHEET, artist_row, ["D", "E"], ["", ""])
    artist.set_daily_counter(0)

  return discord.Embed(title=title, description=description, color=color)

def get_collection(user):
  artist = ARTISTS[user.name]
  collection = artist.get_daily_collection()

  if len(collection) == 0:
    title = "YOU DON'T HAVE MEMBERS COLLECTED YET :confounded:"
    description = ":bangbang: Start collecting with **~greeting** :bangbang:"
    color = discord.Color.random()
    return discord.Embed(title=title, description=description, color=color)
  
  member_counts = {}

  if len(collection) == 0:
    return ""

  # collection: [ () ]

  member_cares = defaultdict(list)
  for member in collection:
    m = member[0]
    d = member[1]
    if m in member_counts:
      member_counts[m] += 1
      if member[1] > member_cares[m][1]:
        member_cares[m][1] = d
    else:
      member_counts[m] = 1
      member_cares[m] = [d, d]

  embed = discord.Embed()
  title = ":sparkling_heart: {0} CARE HISTORY :sparkling_heart:".format(artist.stage_name)
  sorted_members = sorted(member_counts.items(), key=lambda item: -item[1])
  most_caring_member = sorted_members[0][0]
  color = TO1_MEMBERS[most_caring_member].get_embed_color()
  
  # first_care_format = first_care.strftime("%m/%d/%y")
  # last_care_format = None
  # if last_care: #and first_care != last_care:
  #   last_care_format = last_care.strftime("%m/%d/%y")

  for member, count in sorted_members:
    times = "time"
    if count != 1:
      times += "s"
    name = ":heartpulse: {0} {1} {2} {3} :heart_exclamation:".format(member, TO1_MEMBERS[member].get_emoji(), count, times)
    value = ":calendar_spiral: First care: {0}".format(member_cares[member][0].strftime("%m/%d/%y"))

    if member_cares[member][1]:
      value += " | Latest care: {0}".format(member_cares[member][1].strftime("%m/%d/%y"))

    embed.add_field(name=name, value=value, inline=False)
  
  total_cares = sum(list(member_counts.values()))

  if len(sorted_members) > 3 and total_cares > 4:
    embed.add_field(name=("—+" * 10)[:-1], value="\u200B", inline=False)
    name = ":first_place: MOST CARING MEMBER :first_place:"
    value = "hehe **{0}** {1} care you so much :pleading_face:".format(most_caring_member, TO1_MEMBERS[most_caring_member].get_emoji())
    embed.add_field(name=name, value=value)
    embed.set_image(url=TO1_MEMBERS[most_caring_member].get_image())
  
  embed.title = title
  embed.description = ""
  embed.color = discord.Color.from_str(color)
  
  return embed

# group_members is a list of discord member objects
def add_project_to_db(title, leader, category, is_group, release_date, platforms, group_members):
  id = len(PROJECTS) + 1
  gm_names = sorted([gm.name for gm in group_members])
  artists = [ARTISTS[gm] for gm in gm_names]
  project = Project(id, title, leader.name, category, is_group, release_date, platforms, artists)
  PROJECTS[id] = project

  gm_names_string = ",".join(gm_names)
  platforms_string = "+".join(platforms)
  batch_update(PROJECTS_SHEET, id+1, ["A", "H"], [id, title, leader.name, category, is_group, release_date, platforms_string, gm_names_string])
  
  emoji = project.get_emoji()
  title = ":sparkles: PROJECT ADDED :sparkles:"
  description = "{0} ***{1}*** {2}\n".format(emoji, project.get_title().upper(), emoji)
  color = discord.Color.random()
  d = project.get_release_date()
  today = date.today()
  platforms = project.get_platforms()

  if d > today:
    description += ":calendar_spiral: **COMING OUT {0} ON** {1}".format(d.strftime("%m/%d/%y"), platforms)
  elif d == today:
    description += ":calendar_spiral: **OUT TODAY ON** {0}".format(platforms)
  else:
    description += ":calendar_spiral: **RELEASED ON {0} ON** {1}".format(d.strftime("%m/%d/%y"), platforms)

  return discord.Embed(title=title, description=description, color=color)

def _get_projects_by_category(category):
  projects = dict( filter(lambda p: p[1].get_category() == category, PROJECTS.items()) )

  for _, project in PROJECTS:
    if project.get_category() == category:
      projects.append(project)

  return sorted(projects.items(), key=lambda item: int(item))

# TODO: include fields in embed for each project category + solo/group stats
def get_projects():
  if len(PROJECTS) == 1:
    title = "1 PROJECT"
  else:
    title = "{0} PROJECTS".format(len(PROJECTS))

  description = ""
  for project in PROJECTS.values():
    emoji = project.get_emoji()
    t = project.get_title().upper()
    members = ", ".join(project.get_group_members())
    d = project.get_release_date()
    platforms = "+".join(project.get_platforms())
    description += "{0} {1} by {2}, released on {3} via {4}\n".format(emoji, t, members, d, platforms)

  color = discord.Color.random()
  embed = discord.Embed(title=title, description=description, color=color)

  return embed