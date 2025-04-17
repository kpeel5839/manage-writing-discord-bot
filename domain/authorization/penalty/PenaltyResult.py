from domain.Member import Member


class PenaltyResult:

  def __init__(self, member: Member, total_cost: int):
    self.member = member
    self.total_cost = total_cost

  @classmethod
  def of(cls, member: Member, total_cost: int, total_reduce_cost: int):
    return PenaltyResult(member, max(0, total_cost - total_reduce_cost))

  def __str__(self):
    return f"Member {self.member} and total_cost {self.total_cost}"
