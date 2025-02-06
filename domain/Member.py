class Member:

  def __init__(self, id, nick_name, name):
    self.id = id
    self.nick_name = nick_name
    self.name = name

  @classmethod
  def from_with_discord_member(cls, member_in_discord):
    return Member(
        member_in_discord.id,
        member_in_discord.global_name,
        member_in_discord.name
    )

  def __str__(self):
    return f"Member(id={self.id}, nick_name={self.nick_name}, name={self.name})"
