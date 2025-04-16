import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import discord
from discord.ext import commands

from app.Service import set_goal, authorization, mention_who_get_penalty_user, \
  mention_penalty_cost_each_user
from common.Util import get_all_members_in_guild, get_message_in_history, \
  get_or_create_thread
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

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


async def penalty_job():
  channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)
  all_messages_in_channel = await get_message_in_history(channel)
  members = await get_all_members_in_guild(client)
  for each_message in all_messages_in_channel:
    try:
      await mention_who_get_penalty_user(each_message, members)
    except:
      pass


async def start_schedule():
  scheduler = AsyncIOScheduler()
  scheduler.add_job(penalty_job,
                    CronTrigger(
                        hour=0,
                        minute=0,
                        second=1,
                        timezone='Asia/Seoul'
                    ))
  scheduler.start()


@client.event
async def on_ready():
  await start_schedule()
  channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)
  all_messages_in_channel = await get_message_in_history(channel)
  members = await get_all_members_in_guild(client)
  for each_message in all_messages_in_channel:
    try:
      await set_goal(each_message, members)
    except:
      pass
    try:
      await authorization(each_message, members)
    except:
      pass
    try:
      await mention_who_get_penalty_user(each_message, members)
    except Exception as e:
      print(f"Error Reason: {e}")


@client.event
async def on_message(message):
  bot = client.user

  if message.author == bot:
    return

  if message.content.startswith("!목표"):
    await set_goal(message, await get_all_members_in_guild(client))
    return

  if message.content.startswith("!인증"):
    await authorization(message, await get_all_members_in_guild(client))
    return

  if message.content.__eq__("!벌금"):
    channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)
    all_messages_in_channel = await get_message_in_history(channel)
    members = await get_all_members_in_guild(client)
    penalty_messages = await mention_penalty_cost_each_user(
        all_messages_in_channel,
        members
    )
    thread: discord.Thread = await get_or_create_thread(
        message,
        "벌금 고지"
    )

    await thread.send(penalty_messages)
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
