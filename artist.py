"""
The Artist class represents a Discord User. It is separate from the Discord User class, but it takes information from it.
It stores extra information needed for other commands.
"""
from datetime import datetime, timedelta

class Artist:
  def __init__(self, id, name, daily_counter, last_daily_log):
    self.id = id
    self.stage_name = name
    self.emoji = self.__get_user_emoji(name)
    self.daily_collection = [] # [ (member_name, date) ]
    self.daily_counter = daily_counter
    if last_daily_log != "":
      self.last_daily_log = self.__format_date_from_sheets(last_daily_log)
    else:
      self.last_daily_log = ""

  def add_daily_counter(self):
    self.daily_counter += 1
  
  def add_daily(self, member, date):
    self.daily_collection.append( (member, date) )

  def set_daily_collection(self, collection):
    self.daily_collection = collection

  def set_last_daily_log(self, ldl: datetime):
    self.last_daily_log = ldl

  def get_id(self):
    return self.id

  def get_daily_counter(self):
    return self.daily_counter

  def get_daily_collection(self):
    return self.daily_collection

  def __format_date_from_sheets(self, d):
    date_diff = timedelta(days = float(d))
    d = datetime(1899, 12, 30) # google converts date values into ints as a day difference from today to 12/30/1899
    current = d + date_diff
    return current

  def __get_user_emoji(self, name):
    user_info = name.split()
    emoji = user_info[-1]

    if emoji.startswith(":") and emoji.endswith(":"):
      return emoji
    else:
      return None

  def get_last_daily_log(self):
    return self.last_daily_log
