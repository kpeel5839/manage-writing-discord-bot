from domain.Member import Member


class Penalty:

  def __init__(self, member: Member, penalty_cost: int, lack_of_writing: int):
    self.member = member
    self.penalty_cost = penalty_cost
    self.lack_of_writing = lack_of_writing

  @classmethod
  def of(
      cls,
      member: Member,
      penalty_cost: int,
      lack_of_writing: int
  ):
    if penalty_cost < 0 or lack_of_writing < 0:
      return Penalty(member, 0, 0)

    return Penalty(member, penalty_cost, lack_of_writing)

  def get_penalty(self) -> int:
    return self.penalty_cost * self.lack_of_writing

  def __str__(self):
    return f"member_name: {self.member.nick_name} penalty_cost: {self.penalty_cost}, lack_of_writing: {self.lack_of_writing}"
