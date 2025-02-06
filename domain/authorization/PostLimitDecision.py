import discord


class PostLimitDecision:
  KEY_WORD = '!개수'
  LINE = 2

  def __init__(self, limit):
    self.limit = limit

  @classmethod
  def from_with_message(cls, message):
    content = message.content
    limit_line = content.splitlines()[cls.LINE]

    if not limit_line.startswith(cls.KEY_WORD):
      return PostLimitDecision(None)

    try:
      limit = int(limit_line[len(cls.KEY_WORD):].strip())
      return PostLimitDecision(limit)
    except ValueError:
      return PostLimitDecision(None)

  def is_valid(self):
    if self.limit is None:
      return False

    return True

  def __str__(self):
    return f"limit: {self.limit}"
