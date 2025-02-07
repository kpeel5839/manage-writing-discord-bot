import urllib.parse


class URL:
  def __init__(self, url: str):
    self.url = url

  @classmethod
  def create_empty(cls):
    return URL(None)

  @classmethod
  def from_with_row_url(cls, url: str):
    if not url.startswith("https://"):
      return URL(None)

    decoded_url = urllib.parse.unquote(url.strip())
    return URL(decoded_url)

  def is_valid(self):
    return self.url is not None

  def __eq__(self, other):
    return self.url == other

  def __str__(self):
    return self.url
