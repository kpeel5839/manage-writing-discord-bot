from domain.Member import Member
from domain.authorization.penalty.ReducePenalty import ReducePenalty


class ReducePenalties:

  def __init__(
      self,
      member_to_reduce_penalties: dict[Member, list[ReducePenalty]]
  ):
    self.member_to_reduce_penalties = member_to_reduce_penalties

  def add(self, reduce_penalty: ReducePenalty):
    if not reduce_penalty.is_valid():
      return

    if reduce_penalty.member not in self.member_to_reduce_penalties:
      self.member_to_reduce_penalties[reduce_penalty.member] = []

    self.member_to_reduce_penalties[reduce_penalty.member].append(
        reduce_penalty
    )

  def extend(
      self,
      member_to_reduce_penalties: dict[Member, list[ReducePenalty]]
  ):
    for member, members_reduce_penalties in member_to_reduce_penalties.items():

      if member not in self.member_to_reduce_penalties:
        self.member_to_reduce_penalties[member] = []

      for member_reduce_penalty in members_reduce_penalties:
        if member_reduce_penalty.is_valid():
          self.member_to_reduce_penalties[member].append(member_reduce_penalty)

  def total_reduce_cost_by_member(self, member: Member) -> int:
    cost = 0

    if member not in self.member_to_reduce_penalties:
      return 0

    for reduce_penalty in self.member_to_reduce_penalties[member]:
      if reduce_penalty is None:
        continue

      cost += reduce_penalty.cost

    return cost

  def __str__(self):
    return f"member to reduce penalty is {self.member_to_reduce_penalties}"
