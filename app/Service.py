from domain.authorization.WritingAuthorization import WritingAuthorization


async def set_goal(message, members):
  writing_authorization = await WritingAuthorization.of(message, members)
  await writing_authorization.create_thread_with_start_message()


async def authorization(message, members):
  pass


async def mention_who_get_penalty_user(client):
  client.get_channel()
