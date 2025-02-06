class Assignee:
  def __init__(self, assignee):
    self.assignee = assignee

  @classmethod
  def from_with_member(cls, member):
    return Assignee(member)
