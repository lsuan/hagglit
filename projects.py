from datetime import datetime, timedelta

class Project:
  def __init__(self, id, title, leader, category, is_group, release_date, platform):
    self.id = id
    self.title = title
    self.leader = leader
    self.category = category
    self.is_group = is_group
    self.release_date = self.__format_date_from_sheets(release_date)
    self.platform = platform
    self.group_members = []
    self.emoji = self.__set_emoji(category)

  def set_group_members(self, members):
    self.group_members = members

  def get_id(self):
    return self.id

  def get_title(self):
    return self.title

  def get_leader(self):
    return self.leader
  
  def get_category(self):
    return self.category

  def get_members(self):
    pass

  def get_release_date(self):
    return self.release_date

  def get_emoji(self):
    return self.emoji

  def __set_emoji(self, category):
    if category == "dance":
      self.emoji = ":dancer:"
    elif category == "singing":
      self.emoji = ":microphone:"
    elif category == "instrumental":
      self.emoji = ":musical_keyboard:"

  def __format_date_from_sheets(self, d):
    date_diff = timedelta(days = float(d))
    d = datetime(1899, 12, 30) # google converts date values into ints as a day difference from today to 12/30/1899
    current = d + date_diff
    return current