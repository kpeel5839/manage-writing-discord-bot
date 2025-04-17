import discord

from domain.Member import Member


class Members:

  def __init__(self, members: list[Member]):
    self.members = members

  @classmethod
  def from_with_discord_members(cls, members_in_discord: list[discord.Member]):
    members = []
    for member_in_discord in members_in_discord:
      member = Member.from_with_discord_member(member_in_discord)
      members.append(member)

    return Members(members)

  def find_by_member_mention(self, member_mention: str) -> Member:
    for member in self.members:
      mention = member.get_mention()
      if member_mention.__eq__(mention):
        return member

    return None

  def __str__(self):
    return f"Members({self.members})"
