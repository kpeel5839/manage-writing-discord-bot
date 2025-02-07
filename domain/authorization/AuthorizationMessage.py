import discord

from common.Util import is_message_in_thread
from domain.authorization.URL import URL


class AuthorizationMessage:
  KEY_WORD = '!인증'

  def __init__(self, message: discord.Message, link: URL):
    self.message = message
    self.link = link

  @classmethod
  def from_with_message(cls, message: discord.Message):
    if (not is_message_in_thread(message) or
        not message.content.startswith(cls.KEY_WORD)):
      return AuthorizationMessage(message, URL.create_empty())

    link = message.content[len(cls.KEY_WORD):].strip()
    return AuthorizationMessage(message, URL.from_with_row_url(link))

  def is_valid(self):
    return self.link.url is not None

  def __str__(self):
    return f'AuthorizationMessage(message={self.message})'
