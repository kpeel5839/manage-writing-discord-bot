import discord


class DateDecision:
  KEY_WORD = "!기한"
  LINE = 1

  def __init__(self, date):
    self.date = date

  @classmethod
  def from_with_message(cls, message):
    content = message.content
    date_line = content.splitlines()[cls.LINE - 1]

    if not date_line.startswith(cls.KEY_WORD):
      return DateDecision(None)

    try:
      date = discord.utils.parse_time(
          date_line[len(cls.KEY_WORD):].strip()
      )
      return DateDecision(date)
    except ValueError:
      return DateDecision(None)

  def is_valid(self):
    if self.date is None:
      return False

    return True
