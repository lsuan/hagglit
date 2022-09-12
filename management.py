from collections import defaultdict
import discord
from random import randint
from datetime import datetime, date, timedelta
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from artist import Artist
from to1member import TO1Member


def _is_new_day(d: datetime):
  return date.today() > d.date()

# first_attr is the first attribute of the worksheet; the identifier
def _update_db(sheet: gspread.Worksheet, first_attr, col, value):
  sheet_values = sheet.get_values(value_render_option="UNFORMATTED_VALUE")

  row = 2
  for i in range(0, len(sheet_values)):
    if str(sheet_values[i][0]) == first_attr:
      row = i+1
      break
  
  sheet.update_cell(row, col, value)

def _insert(sheet: gspread.Worksheet, col, value):
  sheet_values = sheet.get_all_values()
  empty_cell_row = len(sheet_values)
  sheet.update_cell(empty_cell_row, col, value)

def _batch_insert(sheet: gspread.Worksheet, cols, values):
  sheet_values = sheet.get_values()
  empty_cell_row = len(sheet_values)+1

  cell_range_list = [col + str(empty_cell_row) for col in cols]
  cell_range = cell_range_list[0] + ":" + cell_range_list[-1]
  cells = sheet.range(cell_range)

  for i in range(len(cells)):
    cells[i].value = values[i]
  
  sheet.update_cells(cells)

# cols is a list of letters A-Z that correspond to the spreadsheet
def _batch_update(sheet: gspread.Worksheet, first_attr, cols, values):
  sheet_values = sheet.get_values()+1

  row = 2
  for i in range(len(sheet_values)):
    if values[i][0] == first_attr:
      row = i + 1
      break

  cell_range_list = [col + str(row) for col in cols]
  cell_range = cell_range_list[0] + ":" + cell_range_list[-1]
  cells = sheet.range(cell_range)
  for i in range(len(cells)):
    cells[i].value = values[i]
  
  sheet.update_cells(cells)

def initialize_db():
  scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
  credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
  client = gspread.authorize(credentials)

  # sheet = client.create("Database")
  # sheet.share('Haggethers@gmail.com', perm_type='user', role='writer')
  return client.open("Test Database")

def initialize_to1():
  members_sheet = SHEET_DB.get_worksheet(0)
  members_records = members_sheet.get_all_records()
  to1_members = {}

  for member in members_records:
    to1_members[member["name"]] = TO1Member(member["name"], member["emoji"], member["embed_color"], member["image"])
  
  return to1_members

def initialize_artists():
  artists_sheet = SHEET_DB.get_worksheet(1)
  collections_sheet = SHEET_DB.get_worksheet(2)
  artists_records = artists_sheet.get_all_records(default_blank="", value_render_option="UNFORMATTED_VALUE")
  collections_records = collections_sheet.get_all_records(value_render_option="UNFORMATTED_VALUE")
  
  artists = {}
  artists_ids = {}
  for artist in artists_records:
    counter = None
    if artist["daily_counter"] == "":
      counter = 0
    else:
      counter = artist["daily_counter"]
    artists[artist["name"]] = Artist(str(artist["id"]).lower(), artist["stage_name"], counter, artist["last_daily_log"])
    artists_ids[str(artist["id"]).lower()] = artist["name"]

  for artist in artists.values():
    ldl = artist.get_last_daily_log()
    if ldl != "":
      date_diff = timedelta(days = float(ldl))
      date = datetime(1899, 12, 30) # google converts date values into ints as a day difference from today to 12/30/1899
      current = date + date_diff
      if _is_new_day(current):
        _update_db(artists_sheet, artist.get_id(), 4, 0)

  artists_collections = defaultdict(list)
  for cr in collections_records:
    artists_collections[str(cr["uid"])].append( (cr["member_name"], datetime.strptime(cr["date_received"], "%m/%d/%y").date()) )

  for id, collection in artists_collections.items():
    artist_name = artists_ids[id]
    artists[artist_name].set_daily_collection(collection)  

  return artists

# def initialize_to1():
#   TO1_MEMBERS["Donggeon"] = TO1Member("Donggeon", ":lion_face:", "#d42040", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469434874134549/Donggeon.jpeg")
#   TO1_MEMBERS["Jisu"] = TO1Member("Jisu", ":turtle:", "#d5bc2d", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469435331317830/Jisu.jpeg")
#   TO1_MEMBERS["Jaeyun"] = TO1Member("Jaeyun", ":teddy_bear:", "#d63b3a", "https://media.discordapp.net/attachments/1018469333522972692/1018469435121606747/Jaeyun.jpeg")
#   TO1_MEMBERS["J.You"] = TO1Member("J.You", ":dragon:", "#987c8b", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469435603959928/JYou.jpeg")
#   TO1_MEMBERS["Kyungho"] = TO1Member("Kyungho", ":black_cat:", "#5a995c", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469435851415572/Kyungho.jpeg")
#   TO1_MEMBERS["Daigo"] = TO1Member("Daigo", ":flame:", "#e88367", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469434572156958/Daigo.jpeg")
#   TO1_MEMBERS["Renta"] = TO1Member("Renta", ":smiling_imp:", "#e72339", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469436111466586/Renta.jpeg")
#   TO1_MEMBERS["Yeojeong"] = TO1Member("Yeojeong", ":man_fairy:", "#e9975b", "https://cdn.discordapp.com/attachments/1018469333522972692/1018469436421853194/Yeojeong.jpeg")

# def initialize_artists(guild):
#   for gm in guild.members:
#     if not gm.bot:
#       ARTISTS[gm] = Artist(gm)

SHEET_DB = initialize_db()
TO1_MEMBERS = initialize_to1()
ARTISTS = initialize_artists()

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

def test():
  artist_sheet = SHEET_DB.get_worksheet(1)
  collections_sheet = SHEET_DB.get_worksheet(2)
  v = artist_sheet.get_values()

def get_greeting(user):
  index = randint(0, len(TO1_MEMBERS.keys())-1)
  member = list(TO1_MEMBERS.keys())[index]
  artist = ARTISTS[user.name]
  artist_sheet = SHEET_DB.get_worksheet(1)
  collections_sheet = SHEET_DB.get_worksheet(2)
  artist_id = artist.get_id()

  artist.add_daily_counter()
  _update_db(artist_sheet, artist_id, 4, artist.get_daily_counter())

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
      description = "LMAO I GIVE UP"
    
    return discord.Embed(title=title, description=description, color=color)
    
  artist.add_daily( member, date.today() )
  artist.set_last_daily_log( date.today() )
  today = date.today().strftime("%m/%d/%y")
  
  _update_db(artist_sheet, artist_id, 5, today)
  _batch_insert(collections_sheet, ["A", "B", "C"], [float(artist_id), member, today])
  
  title = ":sparkling_heart: TO: {0} :sparkling_heart:".format(artist.stage_name)
  description = "{0}아 안녕~\n오늘도 beautiful day 하겠다 ^^ 사랑해 :smiling_face_with_3_hearts:\n".format(artist.stage_name)
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
  artist = ARTISTS[user.name]
  collection = artist.get_daily_collection()

  if len(collection) == 0:
    title = "YOU DON'T HAVE MEMBERS COLLECTED YET :confounded:"
    description = ":bangbang: Start collecting with **~greeting** :bangbang:"
    color = discord.Color.random()
    return discord.Embed(title=title, description=description, color=color)
  
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

  embed = discord.Embed()
  title = ":sparkling_heart: {0} CARE HISTORY :sparkling_heart:".format(artist.stage_name)
  sorted_members = sorted(member_counts.items(), key=lambda item: -item[1])
  most_caring_member = sorted_members[0][0]
  color = TO1_MEMBERS[most_caring_member].get_embed_color()
  
  first_care_format = first_care.strftime("%m/%d/%y")
  last_care_format = None
  
  if last_care: #and first_care != last_care:
    last_care_format = last_care.strftime("%m/%d/%y")

  for member, count in sorted_members:
    times = "time"
    if count != 1:
      times += "s"
    name = ":heartpulse: {0} {1} {2} {3} :heart_exclamation:".format(member, TO1_MEMBERS[member].get_emoji(), count, times)
    value = ":calendar_spiral: First care: {0}".format(first_care_format)

    if last_care_format:
      value += " | Latest care: {0}".format(last_care_format)

    embed.add_field(name=name, value=value, inline=False)
  
  total_cares = sum(list(member_counts.values()))

  if len(sorted_members) > 3 and total_cares > 4:
    embed.add_field(name="\u200B", value="\u200B", inline=False)
    name = ":first_place: MOST CARING MEMBER :first_place:"
    value = "hehe **{0}** {1} care you so much :pleading_face:".format(most_caring_member, TO1_MEMBERS[most_caring_member].get_emoji())
    embed.add_field(name=name, value=value)
    embed.set_image(url=TO1_MEMBERS[most_caring_member].get_image())
  
  embed.title = title
  embed.description = ""
  embed.color = discord.Color.from_str(color)
  
  return embed