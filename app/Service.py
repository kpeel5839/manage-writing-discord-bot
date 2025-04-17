import discord

from domain.Members import Members
from domain.authorization.penalty.Penalties import Penalties
from domain.authorization.penalty.PenaltyResult import PenaltyResult
from domain.authorization.penalty.ReducePenalties import ReducePenalties
from domain.authorization.penalty.ReducePenalty import ReducePenalty
from domain.authorization.WritingAuthorization import WritingAuthorization


async def set_goal(message: discord.Message, members: discord.Member):
  writing_authorization = await WritingAuthorization.of(message, members)
  await writing_authorization.create_thread_with_start_message()


async def authorization(
    thread_message: discord.Message,
    members: discord.Member
):
  writing_authorization = await WritingAuthorization.of_by_thread_message(
      thread_message,
      members,
      True
  )
  await writing_authorization.authorize_member(thread_message)


async def mention_who_get_penalty_user(
    message: discord.Message,
    members: discord.Member
):
  writing_authorization = await WritingAuthorization.of(
      message,
      members,
  )
  await writing_authorization.mention_penalty_to_user()


async def mention_penalty_cost_each_user(
    discord_messages: list[discord.Message],
    discord_members: list[discord.Member],
):
  penalties = Penalties({})
  reduce_penalties = ReducePenalties({})
  members: Members = Members.from_with_discord_members(discord_members)

  for discord_message in discord_messages:
    try:
      writing_authorization = await WritingAuthorization.of(
          discord_message,
          discord_members,
      )
      penalties_in_thread = writing_authorization.get_penalties()
      penalties.extend(penalties_in_thread.member_to_penalties)
    except Exception as e:
      print(f"exception occured: {e}")
      pass

    try:
      reduce_penalty = ReducePenalty.from_with_message(discord_message, members)
      reduce_penalties.add(reduce_penalty)
    except Exception as e:
      print(f"exception occured: {e}")
      pass

  penalty_results: list[PenaltyResult] = penalties.get_total_penalty(
      reduce_penalties
  )

  penalty_messages: list[str] = ["벌금 현황입니다"]
  all_of_member_penalty_cost = 0

  for penalty_result in penalty_results:
    all_of_member_penalty_cost += penalty_result.total_cost

    penalty_messages.append(
        f"{penalty_result.member.get_mention()}님의 벌금은 {penalty_result.total_cost}원 입니다."
    )

  penalty_messages.append(f"지금까지 총 모인 금액은 {all_of_member_penalty_cost}원 입니다.")

  return '\n'.join(penalty_messages)
