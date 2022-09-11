"""
The Artist class represents a Discord User. It is separate from the Discord User class, but it takes information from it.
It stores extra information needed for other commands.
"""
class Artist:
  def __init__(self, user):
    self.stage_name = user.display_name
    self.emoji = self.__get_user_emoji(user)
    self.daily_collection = [] # [ (member_name, date) ]
  
  def add_daily(self, member, date):
    self.daily_collection.append( (member, date) )

  def get_daily_collection(self):
    return self.daily_collection

  def __get_user_emoji(self, user):
    user_info = user.display_name.split()
    emoji = user_info[-1]

    if emoji.startswith(":") and emoji.endswith(":"):
      return emoji
    else:
      return None
