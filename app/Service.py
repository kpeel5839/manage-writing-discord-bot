import discord

from domain.authorization.WritingAuthorization import WritingAuthorization


async def set_goal(message: discord.Message, members: discord.Member):
  writing_authorization = await WritingAuthorization.of(message, members)
  await writing_authorization.create_thread_with_start_message()


async def authorization(
    thread_message: discord.Message,
    members: discord.Member
):
  writing_authorization = await WritingAuthorization.of_by_thread_message(
      thread_message,
      members,
      True
  )
  await writing_authorization.authorize_member(thread_message)


async def mention_who_get_penalty_user(
    message: discord.Message,
    members: discord.Member
):
  writing_authorization = await WritingAuthorization.of(
      message,
      members,
  )
  await writing_authorization.mention_penalty_to_user()
