import discord

from common.Util import is_message_in_thread
from domain.authorization.WritingAuthorization import WritingAuthorization


async def set_goal(message: discord.Message, members: discord.Member):
  writing_authorization = await WritingAuthorization.of(message, members)
  await writing_authorization.create_thread_with_start_message()


async def authorization(
    thread_message: discord.Message,
    members: discord.Member
):
  if not is_message_in_thread(thread_message):
    return

  thread = thread_message.channel
  parent_message_property = thread.parent

  parent_message = await parent_message_property.fetch_message(thread.id)

  writing_authorization = await WritingAuthorization.of(
      parent_message,
      members,
      True
  )
  await writing_authorization.authorize_member(thread_message)


async def mention_who_get_penalty_user(client):
  client.get_channel()
