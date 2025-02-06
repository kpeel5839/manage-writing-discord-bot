import discord

from domain.authorization.Assignees import Assignees
from domain.authorization.AuthorizationThread import AuthorizationThread
from domain.authorization.DateDecision import DateDecision
from domain.authorization.PostLimitDecision import PostLimitDecision


class WritingAuthorization:
  THREAD_NAME = "{}까지 화이팅!"
  START_MESSSAGE_PREFIX = "목표를 설정합니다."
  START_MESSSAGE = "{} 기한은 {} 이고, 총 {} 개의 글을 작성하셔야 합니다. {} 화이팅!"

  def __init__(
      self,
      original_message: discord.Message,
      date_decision: DateDecision,
      post_limit_decision: PostLimitDecision,
      assignees: Assignees,
      authorization_thread: AuthorizationThread,
  ):
    self.original_message = original_message
    self.date_decision = date_decision
    self.post_limit_decision = post_limit_decision
    self.assignees = assignees
    self.authorization_thread = authorization_thread

  @classmethod
  async def of(cls, message, members):
    return WritingAuthorization(
        message,
        DateDecision.from_with_message(message),
        PostLimitDecision.from_with_message(message),
        Assignees.from_with_message_and_members(message, members),
        await AuthorizationThread.from_with_message(message),
    )

  async def create_thread_with_start_message(self):
    if (not self.is_valid_message()
        or
        self.authorization_thread.already_exists_content_with_prefix(
            self.START_MESSSAGE_PREFIX
        )):
      return

    thread_name = self.THREAD_NAME.format(self.date_decision.date)
    thread: discord.Thread = await self.original_message.create_thread(
        name=thread_name
    )
    start_message = self.START_MESSSAGE.format(
        self.START_MESSSAGE_PREFIX,
        self.date_decision,
        self.post_limit_decision.limit,
        self.assignees.assignees_nick_names(),
    )
    await thread.send(start_message)

  def is_valid_message(self):
    return self.date_decision.is_valid() and self.post_limit_decision.is_valid() and self.assignees.is_valid()

  def authorize_member(self):
    if self.is_valid_message():
      return

  def mention_penalty_to_user(self):
    if self.is_valid_message():
      return

  def __str__(self):
    return f'WritingAuthorization(date_decision={self.date_decision}, post_limit_decision={self.post_limit_decision}, assignees={self.assignees}, authorization_thread={self.authorization_thread})'
