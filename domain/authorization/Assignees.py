from domain.authorization.Assignee import Assignee
import discord


class Assignees:
  KEY_WORD = '!할당'
  LINE = 3

  def __init__(self, assignees):
    self.assignees = assignees

  @classmethod
  def from_with_message_and_members(cls, message, whole_members):
    content = message.content

    if not content.startswith(cls.KEY_WORD):
      return Assignees([])

    mentions = content[len(cls.KEY_WORD):]

    mentions_without_space = mentions.replace(" ", "")
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
