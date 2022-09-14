from datetime import datetime, timedelta

class Project:
  def __init__(self, id, title, leader, category, is_group, release_date, platform, group_members):
    self.id = id
    self.title = self.__set_title(title)
    self.leader = leader
    self.category = category
    self.is_group = is_group
    
    if release_date != "" and type(release_date) is int:
      self.release_date = self.__format_date_from_sheets(release_date)
    else:
      self.release_date = datetime.strptime(release_date, "%m/%d/%y").date()
    
    self.platform = platform
    self.group_members = sorted(group_members) # [Artist]
    self.emoji = self.__set_emoji(category)

  def set_group_members(self, members):
    self.group_members = sorted(members)

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

  def get_platform(self):
    return self.platform

  def get_emoji(self):
    return self.emoji

  def __set_title(self, title):
    return " ".join(title.split("-"))

  def __set_emoji(self, category):
    if category == "dance-cover":
      self.emoji = ":dancer:"
    elif category == "singing-cover":
      self.emoji = ":microphone:"
    elif category == "instrumental-cover":
      self.emoji = ":musical_keyboard:"
    
    return self.emoji

  def get_group_members(self):
    return self.group_members

  def __format_date_from_sheets(self, d):
    date_diff = timedelta(days = float(d))
    d = datetime(1899, 12, 30) # google converts date values into ints as a day difference from today to 12/30/1899
    current = d + date_diff
    return current.date()