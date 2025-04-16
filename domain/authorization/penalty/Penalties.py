from domain.Member import Member
from domain.authorization.penalty.Penalty import Penalty
from domain.authorization.penalty.PenaltyResult import PenaltyResult
from domain.authorization.penalty.ReducePenalties import ReducePenalties


class Penalties:

  def __init__(self, member_to_penalties: dict[Member, list[Penalty]]):
    self.member_to_penalties = member_to_penalties

  def add(self, penalty: Penalty):
    if penalty.member not in self.member_to_penalties:
      self.member_to_penalties[penalty.member] = []

    self.member_to_penalties[penalty.member].append(penalty)

  def extend(self, member_to_penalties: dict[Member, list[Penalty]]):
    for member, members_penalties in member_to_penalties.items():
      if member not in self.member_to_penalties:
        self.member_to_penalties[member] = []

      self.member_to_penalties[member].extend(members_penalties)

  def get_total_penalty(self, reduce_penalties: ReducePenalties) -> list[
    PenaltyResult
  ]:
    total_penalties_by_member: list[PenaltyResult] = []

    for member, members_penalties in self.member_to_penalties.items():
      total_penalty_cost = 0

      for penalty in members_penalties:
        total_penalty_cost += penalty.get_penalty()

      total_reduce_penalty_cost = reduce_penalties.total_reduce_cost_by_member(
        member
      )

      penalty_result = PenaltyResult.of(
          member,
          total_penalty_cost,
          total_reduce_penalty_cost
      )
      total_penalties_by_member.append(penalty_result)

    return total_penalties_by_member

  def __str__(self):
    return f"memeber to penalties {self.member_to_penalties.__str__()}"
