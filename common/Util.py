import discord


async def get_message_in_history(have_histories):
  if have_histories is None:
    return []

  histories = have_histories.history(limit=None)
  message = []

  async for history in histories:
    message.append(history)

  message.reverse()
  return message


def is_message_in_thread(message):
  if isinstance(message.channel, discord.Thread):
    return True

  return False


async def get_all_members_in_guild(client):
  members = []

  for guild in client.guilds:
    async for member in guild.fetch_members(limit=None):
      members.append(member)

  return members


async def get_or_create_thread(
    message: discord.Message,
    thread_name: str
):
  existing_thread = discord.utils.get(
      message.channel.threads,
      name=thread_name
  )

  if existing_thread:
    return existing_thread

  return await message.create_thread(
      name=thread_name
  )
