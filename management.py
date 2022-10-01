from math import ceil
from random import randint, choice
from unittest import result
from urllib.parse import urlparse

import discord
import tweepy
import os

from helpers import *

def too_many_args_error(command, params, max, user):
  title = ":bangbang: **WARNING TOO MANY ARGUMENTS** :bangbang:"
  description = f"{user.mention} LEA MICHELE! This command takes {max} argument"
  if max != 1:
    description += "s" 
  
  description += ", but you gave {0} :rage:\n".format(len(params))
  description += "***~{0}*** *{1}*".format( command.name, " ".join(command.clean_params.keys()) )
  color = discord.Color.random()
  embed = discord.Embed(title=title, description=description, color=color)
  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1018469333522972692/1019899888873517127/unknown.png")
  embed.set_footer(icon_url=user.display_avatar, text="Silly Gether :rolling_eyes:")
  return embed
  
def get_slay_percentage(user, emojis):
  percentage = randint(0, 100)
  slay_urls = [
    "https://c.tenor.com/onEIkcOsT5YAAAAC/genshin-impact-ruin-guard.gif",
    "https://c.tenor.com/xtGP-kgXhykAAAAC/slay-happy-doggo.gif",
    "https://c.tenor.com/iEgxpghsdjwAAAAC/cat-kitten.gif",
    "https://c.tenor.com/au_s1dXAdFAAAAAC/slay-miku.gif",
    "https://c.tenor.com/xIVZtDaUPc8AAAAC/rise-and-slay-slay.gif"
  ]
  slay_index = randint(0, 4)
  title = ":nail_care: TO SLAY OR NOT TO SLAY :nail_care:"
  description = "{0}'s :sparkles: *SLAY* :sparkles: percentage is ***{1}%*** ".format(user.display_name, percentage)
  color = discord.Color.random()

  embed = discord.Embed(title=title, description=description, color=color)
  embed.set_image(url=slay_urls[slay_index])

  if percentage == 0:
    embed.set_thumbnail(url=emojis[0].url)
  if percentage < 25:
    embed.set_thumbnail(url=emojis[1].url)
  elif percentage < 50:
    embed.set_thumbnail(url=emojis[2].url)
  elif percentage < 75:
    embed.set_thumbnail(url=emojis[3].url)
  elif percentage < 100:
    embed.set_thumbnail(url=emojis[4].url)
  elif percentage == 100:
    embed.set_thumbnail(url=emojis[5].url)
  
  return embed

def get_answers(user):
  answers = [
    [ "I think that's a GOLDEN idea :thumbsup:",
      "You would absolutely :sparkles: SLAY :sparkles: doing that~",
      "#justslaygendtingz :sunglasses:",
      "What's AFTER LIKE? Not 'no' hehe :white_check_mark:",
      "WHAT A BEAUTIFUL DAY to do that :sunny:",
      "NO MORE X with that! Y you questioning? ZO IT :smiling_imp:",
      "Do it, FLYIN' LIKE BUTTERFLIES, ALWAYS LIKE BUTTERFLIES :butterfly:",
      "DON'T FEAR NOW! Yes! :mega:",
      "WHY NOT :question: :question:",
      "FROM THE MINIMUM TO THE MAX, YES! :chart_with_upwards_trend:",
      "YEAH LET'S GET DUMB, LET'S GET DUMB :zany:",
      "GIVE IT EVERYTHING, ALL IN :100:",
      "HECK YEA CHEERS HO! :beers:"
    ],
    [ "You don't got me DRUMMIN DRUMMIN DRAW with that :x:",
      "I would not SURF ON YOU if you did that :man_surfing:",
      "I GOT A FEELING that you shouldn't :lotus:",
      "Sometimes you shouldn't DROP IT LIKE A HOT SAUCE :rolling_eyes:",
      "You're gonna need a PRAYER if you did that :pray:",
      "Do not CHASE after that! :skull_crossbones:",
      "You better TAKE IT SLOW with that thought :octagonal_sign:",
      "YOU BETTER NOT :ghost: :health_worker:",
      "Please RE:ALIZE that you shouldn't do that :white_circle: :black_circle:",
      "Okay let's think about this STEP BY STEP :thinking_face: ... no",
      "Please FADE that idea AWAY :mirror:",
      "You won't be a SON OF BEAST if you do that :red_car:",
      "TAKE A PAUSE and think again :camera_with_flash:"
    ],
    [ "Hmm ask again :fearful:",
      "I'm not sure, maybe try asking a different member :weary:"
    ]
  ]
  members = list(TO1_MEMBERS.keys())
  member = TO1_MEMBERS[choice(members)]
  answer_index = randint(0,2)
  answer = choice(answers[answer_index])
  title = ":bell: FROM: {0} {1} :bell:".format(member.get_name(), member.get_emoji())
  description =  f"{user.mention}, " + answer + "\nhehe till next time 사랑해~ :sparkling_heart:"
  color = discord.Color.from_str(member.get_embed_color())
  embed = discord.Embed(title=title, description=description, color=color)
  embed.set_thumbnail(url=member.get_image())
  return embed

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
    elif counter == 3:
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
    "2.3440408228921344e+17": { "J.You": "Ray... will you give your purse for Kuya J.You~ :smirk: :blush:"},
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

  if len(sorted_members) > 3 or total_cares > 4:
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

# TODO: include fields in embed for each project category + solo/group stats
def get_projects():
  pages = []
  project_ids = sorted([pid for pid in PROJECTS], key=lambda pid: int(pid))
  
  current_page = 1
  if len(PROJECTS) == 1:
    title = ":video_camera: 1 PROJECT :video_camera:"
  else:
    title = ":video_camera: {0} PROJECTS :video_camera:".format(len(PROJECTS))
    if current_page > 1:
      title += " page {0}".format(current_page)

  num_dance = len([p for p in PROJECTS if PROJECTS[p].get_category() == "dance-cover"])
  num_singing = len([p for p in PROJECTS if PROJECTS[p].get_category() == "singing-cover"])
  num_instrumental = len([p for p in PROJECTS if PROJECTS[p].get_category() == "instrumental-cover"])
  description = "***{} DANCE COVERS :dancer:\n{} SINGING COVERS :microphone:\n{} INSTRUMENTAL COVERS :musical_keyboard:***".format(
                    num_dance, num_singing, num_instrumental
                )

  reps = ceil(len(project_ids) / 10)
  cutoff = 0
  for rep in range(reps):
    color = discord.Color.random()
    embed = discord.Embed(title=title, description=description, color=color)
    for i in range(cutoff, len(project_ids)):
      if i == (10 + cutoff):
        cutoff = i
        current_page += 1
        break
      project = PROJECTS[project_ids[i]]
      id = project.get_id()
      emoji = project.get_emoji()
      t = project.get_title().upper()
      members = [m.get_stage_name() for m in project.get_members()]
      d = project.get_release_date().strftime("%m/%d/%y")
      platforms = "+".join(project.get_platforms())
      name = "{0}. {1} {2}".format(id, t, emoji)
      value = ":bust_in_silhouette: by: {}\n".format(", ".join(members))
      value += ":calendar_spiral: released: {} on {}".format(d, platforms)
      embed.add_field(name=name, value=value)
      if i % 2 == 1:
        embed.add_field(name="\u200B", value="\u200B", inline=False)
    pages.append(embed)
    title = ":video_camera: {0} PROJECTS :video_camera:".format(len(PROJECTS))
    if current_page > 1:
      title += " (page {0})".format(current_page)
    embed = discord.Embed(title=title, description=description, color=color)

  return pages
  # for project in PROJECTS.values():
  #   id = project.get_id()
  #   emoji = project.get_emoji()
  #   t = project.get_title().upper()
  #   members = [ARTISTS[m].get_stage_name() for m in project.get_members()]
  #   d = project.get_release_date()
  #   platforms = "+".join(project.get_platforms())
  #   name = "{0}. {1} {2}".format(id, t, emoji)
  #   value = ":bust_in_silhouette: by: {}\n".format(", ".join(members))
  #   value += ":calendar_spiral: released: {} on {}".format(d, platforms)
  #   # embed.add_field(name=("—+" * 10)[:-1], value="\u200B", inline=False)
  #   embed.add_field(name=name, value=value)
  return embed

def get_twitter_analytics(url):
  api_key = os.getenv("TWITTER_KEY")
  api_key_secret = os.getenv("TWITTER_KEY_SECRET")
  bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
  access_token = os.getenv("TWITTER_ACCESS_TOKEN")
  access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
  
  # [attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld]
  client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)
  tweet_fields = ["public_metrics", "conversation_id"]
  
  tweet_path = urlparse(url).path
  tweet_id = int(tweet_path.split("/")[-1])
  tweet = client.get_tweet(tweet_id, tweet_fields=tweet_fields)
  public_metrics = tweet.data.public_metrics
  public_metrics["total"] = sum(list(public_metrics.values()))
  return public_metrics

def get_project_analytics(user, project, platform, platform_emoji, url):
  project_title = project.get_title().upper()
  if "_" in project_title:
    project_title = " ".join(project_title.split("_"))
  title = "{0} {1} {0} - RELEASED ON {2}".format(project.get_emoji(), project_title, project.get_release_date())
  description = "{0} **ANALYTICS**\n".format(platform_emoji)

  metrics = None
  if platform == "twitter":
    metrics = get_twitter_analytics(url)

  description += ":heart: LIKES = {0}\n".format(metrics["like_count"])
  description += ":thought_balloon: REPLIES = {0}\n".format(metrics["reply_count"])
  description += ":repeat: RETWEETS = {0}\n".format(metrics["retweet_count"])
  description += ":pencil: QUOTES = {0}\n".format(metrics["quote_count"])
  description += ":heavy_equals_sign: TOTAL INTERACTIONS = {0}".format(metrics["total"])

  color = discord.Color.random()
  embed = discord.Embed(title=title, description=description, color=color)
  embed.set_footer(text="Requested by {0}".format(user.display_name), icon_url=user.display_avatar.url)
  return embed

def help_commands(commands, user):
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
    _get_commands_info(embed, care_title, "", care_commands)
  embed.add_field(name=("—+" * 10)[:-1], value="\u200B", inline=False)
  
  if len(project_commands) > 0:
    project_title = ":video_camera: PROJECT COMMANDS :video_camera:"
    _get_commands_info(embed, project_title, "", project_commands)
  embed.add_field(name=("—+" * 10)[:-1], value="\u200B", inline=False)

  if len(misc_commands) > 0:
    misc_title = ":partying_face: MISCELLANEOUS COMMANDS: :partying_face:"
    _get_commands_info(embed, misc_title, "", misc_commands)

  text = f"Requested by {user.display_name}"
  embed.set_footer(icon_url=user.display_avatar, text=text)
  return embed

def _get_commands_info(embed, name, value, commands):
  for command in commands:
    parameters = command.clean_params.values()    
    marked_params = []

    for cp in parameters:
      if cp.kind == 1:
        marked_params.append("**"+cp.name+"**")
      elif cp.kind == 2:
        marked_params.append("*"+cp.name+"*")

    value += ":pushpin: __***~{0}***__ {1}\n".format(command.name, " ".join(marked_params))
    value += ":pencil: {0}\n".format(command.description)
  embed.add_field(name=name, value=value)