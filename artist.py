"""
The Artist class represents a Discord User. It is separate from the Discord User class, but it takes information from it.
It stores extra information needed for other commands.
"""
from xmlrpc.client import DateTime


class Artist:
  def __init__(self, id, name, daily_counter, last_daily_log):
    self.id = id
    self.stage_name = name
    self.emoji = self.__get_user_emoji(name)
    self.daily_collection = [] # [ (member_name, date) ]
    self.daily_counter = daily_counter
    self.last_daily_log = last_daily_log

  def add_daily_counter(self):
    self.daily_counter += 1
  
  def add_daily(self, member, date):
    self.daily_collection.append( (member, date) )

  def set_daily_collection(self, collection):
    self.daily_collection = collection

  def set_last_daily_log(self, date: DateTime):
    self.last_daily_log = date

  def get_id(self):
    return self.id

  def get_daily_counter(self):
    return self.daily_counter

  def get_daily_collection(self):
    return self.daily_collection

  def __get_user_emoji(self, name):
    user_info = name.split()
    emoji = user_info[-1]

    if emoji.startswith(":") and emoji.endswith(":"):
      return emoji
    else:
      return None

  def get_last_daily_log(self):
    return self.last_daily_log
