import discord

from domain.Member import Member
from domain.Members import Members


class ReducePenalty:
  KEY_WORD = '!벌금삭감'

  def __init__(self, member: Member, cost: int):
    self.member = member
    self.cost = cost

  @classmethod
  def from_with_message(cls, message: discord.Message, members: Members):
    content = message.content

    if not content.startswith(cls.KEY_WORD):
      return ReducePenalty(None, 0)

    components: list[str] = content.split(" ")

    if len(components) <= 2:
      return ReducePenalty(None, 0)

    member_mention = components[1]
    member = members.find_by_member_mention(member_mention)
    cost = int(components[2])

    return ReducePenalty(member, cost)

  def is_valid(self):
    return self.member is not None

  def __str__(self):
    return f"member {self.member} cost is {self.cost}"
