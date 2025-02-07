import discord

from domain.authorization.Assignees import Assignees
from domain.authorization.AuthorizationMessage import AuthorizationMessage
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
  async def of(cls,
      message,
      members,
      removed_latest_message_for_authorization: bool = False
  ):
    authorization_thread = await AuthorizationThread.from_with_message(message)

    authorization_messages = authorization_thread.get_authorization_messages_in_thread(
        removed_latest_message_for_authorization
    )

    assignees = Assignees.from_with_message_and_members(message, members)
    for authorization_message in authorization_messages:
      await assignees.authorize_link_by_message(authorization_message)

    return WritingAuthorization(
        message,
        DateDecision.from_with_message(message),
        PostLimitDecision.from_with_message(message),
        assignees,
        authorization_thread
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

  async def authorize_member(self, message: discord.Message):
    if not self.is_valid_message():
      return

    authorization_message = AuthorizationMessage.from_with_message(message)
    await self.assignees.authorize_link_by_message(
        authorization_message,
        self.post_limit_decision.limit,
        True
    )

  def mention_penalty_to_user(self):
    if not self.is_valid_message():
      return

  def __str__(self):
    return f'WritingAuthorization(date_decision={self.date_decision}, post_limit_decision={self.post_limit_decision}, assignees={self.assignees}, authorization_thread={self.authorization_thread})'
