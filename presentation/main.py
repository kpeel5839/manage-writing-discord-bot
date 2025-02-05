import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True  # 권한 허용

client = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("DISCORD_TOKEN")
AUTHORIZATION_CHANNEL_ID = int(os.getenv("AUTHORIZATION_CHANNEL_ID"))

@client.event
async def on_ready():
  channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)
  history = channel.history(limit=None)
  message = []
  async for msg in history:
    message.append(msg)
  for guild in client.guilds:
    await channel.send(f"서버 이름: {guild.name}")
    async for member in guild.fetch_members(limit=None):
      await channel.send(
          f"사용자 이름: {member.global_name} and id: {member.id}"
      )
      await channel.send(
          f"{member.avatar}"
      )


@client.command(name="인증")
async def reply_here(ctx):
  if isinstance(ctx.channel, discord.Thread):  # 현재 채널이 스레드인지 확인
    await ctx.send(f"✅ `{ctx.command}` 명령어가 스레드에서 실행되었습니다!")
    await ctx.message.reply(
        f"👍 `{ctx.command}` 명령어가 스레드에서 실행되었습니다! {ctx.message.content}",
        mention_author=True
    )
    thread = ctx.channel
    messages = []
    async for msg in thread.history(limit=None):
      messages.append(msg)
    print(messages)
  else:
    await ctx.send("⚠️ 이 명령어는 스레드에서 실행해야 합니다.")


@client.event
async def on_message(message):  # 모든 메시지 트래킹
  bot = client.user
  if message.author == bot:
    return
  if message.channel.id != AUTHORIZATION_CHANNEL_ID:
    return

  channel = client.get_channel(AUTHORIZATION_CHANNEL_ID)
  await channel.send(f"[{message.channel}] {message.author}: {message.content}")

  # 명령어가 있는 경우, 기존의 명령어 핸들러를 실행하도록 설정
  await client.process_commands(message)


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
