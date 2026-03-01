import re
import urllib.parse
from html.parser import HTMLParser
from curl_cffi.requests import AsyncSession


class ContentStatus:
  VALID = "valid"
  NOT_FOUND = "not_found"
  INSUFFICIENT = "insufficient"
  UNREACHABLE = "unreachable"


SPA_MARKERS = {'javascript must be enabled', 'enable javascript', 'requires javascript'}


class _TextExtractor(HTMLParser):
  SKIP_TAGS = {'script', 'style', 'nav', 'header', 'footer'}
  BLOCK_TAGS = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'br', 'tr'}
  MIN_LINE_LENGTH = 20

  def __init__(self):
    super().__init__()
    self._parts = []
    self._skip_depth = 0

  def handle_starttag(self, tag, attrs):
    if tag in self.SKIP_TAGS:
      self._skip_depth += 1
    elif tag in self.BLOCK_TAGS:
      self._parts.append('\n')

  def handle_endtag(self, tag):
    if tag in self.SKIP_TAGS:
      self._skip_depth = max(0, self._skip_depth - 1)

  def handle_data(self, data):
    if self._skip_depth == 0:
      self._parts.append(data)

  def get_meaningful_lines(self):
    text = ''.join(self._parts)
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if len(line) >= self.MIN_LINE_LENGTH]


class URL:
  MINIMUM_CONTENT_LINES = 5
  FETCH_TIMEOUT = 10

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

  async def fetch_content_status(self) -> str:
    if not self.is_valid():
      return ContentStatus.NOT_FOUND

    try:
      async with AsyncSession() as session:
        response = await session.get(
            self.url,
            impersonate="chrome",
            timeout=self.FETCH_TIMEOUT
        )

        if response.status_code == 404:
          return ContentStatus.NOT_FOUND
        if response.status_code != 200:
          return ContentStatus.UNREACHABLE

        html = response.text

        title_match = re.search(r'<title[^>]*>([^<]*)</title>', html, re.IGNORECASE)
        if title_match and '404' in title_match.group(1):
          return ContentStatus.NOT_FOUND

        if any(marker in html.lower() for marker in SPA_MARKERS):
          return ContentStatus.VALID

        extractor = _TextExtractor()
        extractor.feed(html)
        lines = extractor.get_meaningful_lines()

        if len(lines) <= self.MINIMUM_CONTENT_LINES:
          return ContentStatus.INSUFFICIENT

        return ContentStatus.VALID
    except Exception:
      return ContentStatus.UNREACHABLE

  def is_valid(self):
    return self.url is not None

  def __eq__(self, other):
    return self.url == other

  def __str__(self):
    return self.url
