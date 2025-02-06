import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import discord
from discord.ext import commands

from app.Service import set_goal
from common.Util import get_all_members_in_guild, get_message_in_history, \
  is_message_in_thread

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True
intents.guilds = True
intents.typing = False
intents.presences = False
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
AUTHORIZATION_CHANNEL_ID = int(os.getenv("AUTHORIZATION_CHANNEL_ID"))


@client.event
async def on_ready():
  channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)
  all_messages_in_channel = await get_message_in_history(channel)
  members = await get_all_members_in_guild(client)
  for each_message in all_messages_in_channel:
    try:
      if not is_message_in_thread(each_message):
        await set_goal(each_message, members)
    except:
      pass


# @client.command(name="인증")
# async def reply_here(ctx):
#   if isinstance(ctx.channel, discord.Thread):  # 현재 채널이 스레드인지 확인
#     await ctx.send(f"✅ `{ctx.command}` 명령어가 스레드에서 실행되었습니다!")
#     await ctx.message.reply(
#         f"👍 `{ctx.command}` 명령어가 스레드에서 실행되었습니다! {ctx.message.content}",
#         mention_author=True
#     )
#     thread = ctx.channel
#     messages = await get_message_in_history(thread)
#     await ctx.message.reply(messages.__str__()[:2000])
#   else:
#     await ctx.send("⚠️ 이 명령어는 스레드에서 실행해야 합니다.")


@client.event
async def on_message(message):
  bot = client.user

  if message.author == bot:
    return

  if message.content.startswith("!목표") and not is_message_in_thread(message):
    await set_goal(message, await get_all_members_in_guild(client))
    return

  await client.process_commands(message)


@client.command(name="하영")
async def hayong(ctx):
  await ctx.send("귀여워!")


@client.command(name="해피쿠킹")
async def happy_cooking(ctx):
  await ctx.send("최고의 키보드!")


@client.command(name="민희")
async def minhee(ctx):
  await ctx.send("탐켄치야 힘내!!!")


@client.command(name="매튜")
async def matthew(ctx):
  await ctx.send("코딩 고수")


client.run(TOKEN)
