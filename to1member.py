from discord import embeds


class TO1Member:
  def __init__(self, name, emoji, embed_color, image):
    self.name = name
    self.emoji = emoji
    self.embed_color = embed_color
    self.image = image
  
  def get_name(self):
    return self.name
  
  def get_emoji(self):
    return self.emoji
  
  def get_embed_color(self):
    return self.embed_color

  def get_image(self):
    return self.image

