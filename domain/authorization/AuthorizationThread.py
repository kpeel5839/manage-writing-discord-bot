from common.util import get_message_in_history


class AuthorizationThread:
  def __init__(self, message, thread_messages):
    self.message = message
    self.thread_messages = thread_messages

  @classmethod
  async def from_with_message(cls, message):
    thread_channel = message.channel
    threads = await get_message_in_history(thread_channel)
    return AuthorizationThread(message, threads)
