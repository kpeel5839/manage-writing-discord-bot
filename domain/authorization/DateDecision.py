from datetime import datetime

import discord


class DateDecision:
  KEY_WORD = "!기한"
  LINE = 1

  def __init__(self, date):
    self.date = date

  @classmethod
  def from_with_message(cls, message: discord.Message):
    content = message.content
    date_line = content.splitlines()[cls.LINE]

    if not date_line.startswith(cls.KEY_WORD):
      return DateDecision(None)

    try:
      date = datetime.strptime(
          date_line[len(cls.KEY_WORD):].strip(),
          "%Y.%m.%d"
      )
      return DateDecision(date)
    except ValueError:
      return DateDecision(None)

  def is_valid(self):
    if self.date is None:
      return False

    return True

  def __str__(self):
    return str(self.date)

  def time_is_not_over_due_date(self, now_time_in_seoul) -> bool:
    return self.date.date() >= now_time_in_seoul.date()
