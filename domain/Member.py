import discord


class Member:
  MENTION = "<@{}>"

  def __init__(self, id, nick_name, name):
    self.id = id
    self.nick_name = nick_name
    self.name = name

  @classmethod
  def from_with_discord_member(cls, member_in_discord: discord.Member):
    return Member(
        member_in_discord.id,
        member_in_discord.global_name,
        member_in_discord.name
    )

  def get_mention(self) -> str:
    return self.MENTION.format(self.id)

  def __str__(self):
    return f"Member(id={self.id}, nick_name={self.nick_name}, name={self.name})"

  def __eq__(self, other):
    if isinstance(other, Member):
      return self.id == other.id
    return False

  def __hash__(self):
    return hash(self.id)
