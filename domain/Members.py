from domain.Member import Member


class Members:

  def __init__(self, members: list[Member]):
    self.members = members

  @classmethod
  def from_with_discord_members(cls, members_in_discord):
    members = []
    for member_in_discord in members_in_discord:
      member = Member.from_with_discord_member(member_in_discord)
      members.append(member)
    return members

  def __str__(self):
    return f"Members({self.members})"
