from domain.Member import Member
from domain.authorization.URL import URL


class Assignee:
  def __init__(self, assignee: Member, links: list[URL]):
    self.assignee = assignee
    self.links = links

  @classmethod
  def from_with_member(cls, member: Member):
    return Assignee(member, [])

  def authorize_link(self, add_link: URL):
    if add_link in self.links or not add_link.is_valid():
      return False

    self.links.append(add_link)
    return True

  def is_same_id(self, author_id: int):
    return self.assignee.id == author_id

  def written_link(self):
    links = []

    for url in self.links:
      links.append(url.url)

    return ", ".join(links)

  def lack_of_writing(self, limit: int):
    return max(0, limit - len(self.links))

  def __str__(self):
    return str(self.assignee.__str__())
