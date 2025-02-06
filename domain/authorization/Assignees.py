from domain.authorization.Assignee import Assignee


class Assignees:
  KEY_WORD = '!할당'
  LINE = 3

  def __init__(self, assignees: list[Assignee]):
    self.assignees = assignees

  @classmethod
  def from_with_message_and_members(cls, message, whole_members):
    content = message.content
    assignees_line = content.splitlines()[cls.LINE]

    if not assignees_line.startswith(cls.KEY_WORD):
      return Assignees([])

    mentions = assignees_line[len(cls.KEY_WORD):]

    mentions_without_space = (mentions.replace(" ", "")
                              .replace("<", "")
                              .replace(">", ""))
    member_ids = [int(num) for num in mentions_without_space.split('@') if num]

    assignees = []

    for member in whole_members:
      if member_ids.__contains__(member.id):
        assignee = Assignee.from_with_member(member)
        assignees.append(assignee)

    return Assignees(assignees)

  def is_valid(self):
    if len(self.assignees) == 0:
      return False

    return True

  def assignees_nick_names(self):
    names = []
    for assignee in self.assignees:
      names.append(assignee.assignee.name)
    return ", ".join(names)

  def __str__(self):
    nick_names = []
    for assignee in self.assignees:
      nick_names.append(assignee.__str__())
    return f"Assignees(names={nick_names})"
