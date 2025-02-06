async def get_message_in_history(have_histories):
  histories = have_histories.history(limit=None)
  message = []

  async for history in histories:
    message.append(history)

  return message
