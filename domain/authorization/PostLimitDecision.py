import discord


class PostLimitDecision:
  KEY_WORD = '!개수'
  LINE = 2

  def __init__(self, limit):
    self.limit = limit

  @classmethod
  def from_with_message(cls, message):
    content = message.content

    if not content.startswith(cls.KEY_WORD):
      return PostLimitDecision(None)

    try:
      limit = int(content[len(cls.KEY_WORD):].strip())
      return PostLimitDecision(limit)
    except ValueError:
      return PostLimitDecision(None)

  def is_valid(self):
    if self.limit is None:
      return False

    return True
