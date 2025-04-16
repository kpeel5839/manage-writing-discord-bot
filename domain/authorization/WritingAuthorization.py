import datetime
from zoneinfo import ZoneInfo

import discord

from common.Util import is_message_in_thread, get_or_create_thread
from domain.authorization.Assignees import Assignees
from domain.authorization.AuthorizationMessage import AuthorizationMessage
from domain.authorization.AuthorizationThread import AuthorizationThread
from domain.authorization.DateDecision import DateDecision
from domain.authorization.penalty.Penalties import Penalties
from domain.authorization.penalty.Penalty import Penalty
from domain.authorization.PostLimitDecision import PostLimitDecision


class WritingAuthorization:
  THREAD_NAME = "{}까지 화이팅!"
  START_MESSSAGE_PREFIX = "목표를 설정합니다."
  START_MESSSAGE = "{} 기한은 {} 이고, 총 {} 개의 글을 작성하셔야 합니다. {} 화이팅!"
  PENALTY_COST = 10000
  PENALTY_MESSAGE_PREFIX = "<@{}>님 당첨되었습니다."
  PENALTY_MESSAGE = "{} 벌금은 글 하나당 {}원 이며 당신은 {}개 미달했습니다. 고로 벌금은 {}원 입니다."
  DATE_FORMAT = "%Y-%m-%d"

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
  async def of(
      cls,
      message,
      members,
      removed_latest_message_for_authorization: bool = False
  ):
    assert not is_message_in_thread(message), "is in thread message"
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

  @classmethod
  async def of_by_thread_message(
      cls,
      thread_message,
      members: discord.Member,
      removed_latest_message_for_authorization: bool = False
  ):
    assert is_message_in_thread(thread_message), "is not in thread message"
    thread = thread_message.channel
    message_property = thread.parent
    message = await message_property.fetch_message(thread.id)
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

    thread_name = self.THREAD_NAME.format(
        self.date_decision.date.strftime(self.DATE_FORMAT)
    )
    thread: discord.Thread = await get_or_create_thread(
        self.original_message,
        thread_name
    )

    start_message = self.START_MESSSAGE.format(
        self.START_MESSSAGE_PREFIX,
        self.date_decision.date.strftime(self.DATE_FORMAT),
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

  async def mention_penalty_to_user(self):
    message_thread = self.original_message.thread
    now_time_in_seoul = (datetime.datetime.now(ZoneInfo("Asia/Seoul"))
                         .replace(tzinfo=None))
    if not self.is_valid_message() or message_thread is None or self.date_decision.date.date() >= now_time_in_seoul.date():
      return

    for assignee in self.assignees.assignees:
      penalty_prefix = self.PENALTY_MESSAGE_PREFIX.format(assignee.assignee.id)
      remain_writing = assignee.lack_of_writing(self.post_limit_decision.limit)
      if self.authorization_thread.already_exists_content_with_prefix(
          penalty_prefix
      ) or remain_writing == 0:
        continue

      penalty_message = self.PENALTY_MESSAGE.format(
          penalty_prefix,
          self.PENALTY_COST,
          remain_writing,
          remain_writing * self.PENALTY_COST
      )
      await message_thread.send(penalty_message)

  def get_penalties(self) -> Penalties:
    penalties = Penalties({})
    now_time_in_seoul = (datetime.datetime.now(ZoneInfo("Asia/Seoul"))
                         .replace(tzinfo=None))

    if self.date_decision.time_is_not_over_due_date(now_time_in_seoul):
      return penalties

    for assignee in self.assignees.assignees:
      remain_writing = assignee.lack_of_writing(self.post_limit_decision.limit)

      penalty = Penalty.of(
          assignee.assignee,
          self.PENALTY_COST,
          remain_writing
      )

      penalties.add(penalty)

    return penalties

  def __str__(self):
    return f'WritingAuthorization(date_decision={self.date_decision}, post_limit_decision={self.post_limit_decision}, assignees={self.assignees}, authorization_thread={self.authorization_thread})'
