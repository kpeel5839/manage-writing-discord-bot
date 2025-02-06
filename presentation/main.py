import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import discord
from discord.ext import commands

from common.util import get_message_in_history

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True
intents.guilds = True
intents.typing = False
intents.presences = False
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

# TOKEN = os.getenv("DISCORD_TOKEN")
# AUTHORIZATION_CHANNEL_ID = int(os.getenv("AUTHORIZATION_CHANNEL_ID"))


@client.event
async def on_ready():
  channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)
  await channel.send("Bot is ready!")

  # messages = await get_message_in_history(channel)
  # await channel.send(messages.__str__()[:2000])

  # for guild in client.guilds:
  #   await channel.send(f"서버 이름: {guild.name}")
  #   async for member in guild.fetch_members(limit=None):
  #     await channel.send(
  #         f"사용자 이름: {member.global_name} and id: {member.id}"
  #     )
  #     await channel.send(
  #         f"{member.avatar}"
  #     )


@client.command(name="인증")
async def reply_here(ctx):
  if isinstance(ctx.channel, discord.Thread):  # 현재 채널이 스레드인지 확인
    await ctx.send(f"✅ `{ctx.command}` 명령어가 스레드에서 실행되었습니다!")
    await ctx.message.reply(
        f"👍 `{ctx.command}` 명령어가 스레드에서 실행되었습니다! {ctx.message.content}",
        mention_author=True
    )
    thread = ctx.channel
    messages = await get_message_in_history(thread)
    await ctx.message.reply(messages.__str__()[:2000])
  else:
    await ctx.send("⚠️ 이 명령어는 스레드에서 실행해야 합니다.")


@client.event
async def on_message(message):  # 모든 메시지 트래킹
  bot = client.user
  channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)

  if message.author == bot:
    return

  await channel.send(f"[{message.channel}] {message.author}: {message.content}")
  await client.process_commands(message)

  if message.content.startswith("!인증"):
    if isinstance(message.channl, discord.Thread):  # 현재 채널이 스레드인지 확인
      await channel.send(f"✅ `{message.command}` 명령어가 스레드에서 실행되었습니다!")
      await message.reply(
          f"👍 `{message.command}` 명령어가 스레드에서 실행되었습니다! {message.content}",
          mention_author=True
      )
      thread = message.channel
      messages = await get_message_in_history(thread)
      for msg in messages:
        await message.reply(msg.content)


@client.command(name="하영")
async def hayong(ctx):
  await ctx.send("귀여워!")


@client.command(name="해피쿠킹")
async def happy_cooking(ctx):
  await ctx.send("최고의 키보드!")


@client.command(name="민희")
async def minhee(ctx):
  await ctx.send("탐켄치")


client.run(TOKEN)
