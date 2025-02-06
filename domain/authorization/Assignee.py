from domain.Member import Member


class Assignee:
  def __init__(self, assignee: Member):
    self.assignee = assignee

  @classmethod
  def from_with_member(cls, member: Member):
    return Assignee(member)

  def __str__(self):
    return str(self.assignee.__str__())
