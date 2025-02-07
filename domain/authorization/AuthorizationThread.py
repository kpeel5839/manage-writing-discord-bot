from common.Util import get_message_in_history
from domain.authorization.AuthorizationMessage import AuthorizationMessage


class AuthorizationThread:
  def __init__(self, message, thread_messages):
    self.message = message
    self.thread_messages = thread_messages

  @classmethod
  async def from_with_message(cls, message):
    thread = message.thread

    if thread is None:
      return AuthorizationThread(message, [])

    thread_messages = await get_message_in_history(thread)
    return AuthorizationThread(message, thread_messages)

  def already_exists_content_with_prefix(self, prefix: str):
    for message in self.thread_messages:
      if message.content.startswith(prefix):
        return True
    return False

  def get_authorization_messages_in_thread(
      self,
      removed_latest_message: bool = False
  ):
    messages = []

    for thread_message in self.thread_messages:
      authorization_message = AuthorizationMessage.from_with_message(
          thread_message
      )
      if authorization_message.is_valid():
        messages.append(authorization_message)

    if removed_latest_message:
      return messages[:-1]

    return messages

  def __str__(self):
    return f'AuthorizationThread(message={self.message}, thread_messages={self.thread_messages})'
