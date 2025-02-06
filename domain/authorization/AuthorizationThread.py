from common.util import get_message_in_history


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
    print(prefix)
    for message in self.thread_messages:
      print(message.content)
      if message.content.startswith(prefix):
        return True
    return False

  def __str__(self):
    return f'AuthorizationThread(message={self.message}, thread_messages={self.thread_messages})'
