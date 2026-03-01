import discord

from domain.Member import Member
from domain.authorization.Assignee import Assignee
from domain.authorization.AuthorizationMessage import AuthorizationMessage
from domain.authorization.URL import ContentStatus


class Assignees:
  KEY_WORD = '!할당'
  LINE = 3
  FAILED_AUTHORIZATION_MESSAGE = "이미 사용하거나 올바르지 않은 링크입니다 {}님"
  SUCCESS_AUTHORIZATION_MESSAGE = "{}님, 현재까지 {}로, {}개의 글을 쓰셨고, {}개 남았습니다."
  NOT_FOUND_CONTENT_MESSAGE = "{}님, 링크에 접근할 수 없습니다. 콘텐츠가 게시된 후 다시 시도해주세요."
  INSUFFICIENT_CONTENT_MESSAGE = "{}님, 콘텐츠가 너무 부실합니다. 충분한 내용을 작성한 뒤 다시 시도해주세요."

  def __init__(self, assignees: list[Assignee]):
    self.assignees = assignees

  @classmethod
  def from_with_message_and_members(
      cls,
      message,
      whole_members: discord.Member
  ):
    content = message.content
    assignees_line = content.splitlines()[cls.LINE]

    if not assignees_line.startswith(cls.KEY_WORD):
      return Assignees([])

    mentions = assignees_line[len(cls.KEY_WORD):]
    mentions_without_space = (mentions.replace(" ", "")
                              .replace("<", "")
                              .replace(">", ""))
    member_ids = [int(num) for num in mentions_without_space.split('@') if num]
    assignees = []

    for member in whole_members:
      if member_ids.__contains__(member.id):
        assignee = Assignee.from_with_member(
            Member.from_with_discord_member(member)
        )
        assignees.append(assignee)

    return Assignees(assignees)

  def is_valid(self):
    if len(self.assignees) == 0:
      return False

    return True

  def assignees_nick_names(self):
    names = []
    for assignee in self.assignees:
      names.append(assignee.assignee.name)
    return ", ".join(names)

  async def authorize_link_by_message(
      self,
      authorization_message: AuthorizationMessage,
      writing_goal: int = 0,
      send_message: bool = False
  ):
    message = authorization_message.message
    for assignee in self.assignees:
      if not assignee.is_same_id(message.author.id):
        continue

      if authorization_message.link.is_valid():
        content_status = await authorization_message.link.fetch_content_status()

        if content_status in (ContentStatus.NOT_FOUND, ContentStatus.UNREACHABLE):
          if send_message:
            await message.reply(
                self.NOT_FOUND_CONTENT_MESSAGE.format(assignee.assignee.name)
            )
          return

        if content_status == ContentStatus.INSUFFICIENT:
          if send_message:
            await message.reply(
                self.INSUFFICIENT_CONTENT_MESSAGE.format(assignee.assignee.name)
            )
          return

      is_successful_add = assignee.authorize_link(authorization_message.link)

      if not send_message:
        return

      if not is_successful_add:
        await message.reply(
            self.FAILED_AUTHORIZATION_MESSAGE.format(assignee.assignee.name)
        )
        return

      await message.reply(self.SUCCESS_AUTHORIZATION_MESSAGE.format(
          assignee.assignee.name,
          assignee.written_link(),
          len(assignee.links),
          max(0, writing_goal - len(assignee.links))
      ))
      return

  def __str__(self):
    nick_names = []
    for assignee in self.assignees:
      nick_names.append(assignee.__str__())
    return f"Assignees(names={nick_names})"
