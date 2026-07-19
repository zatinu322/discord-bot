import asyncio
import logging
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from orm.repository.drunkard import get_drunkard_by_id

if TYPE_CHECKING:
    from discord import Member
    from discord.role import Role

    from bot import Bot
    from orm.models import Drunkard

logger = logging.getLogger(__file__)


async def set_role(
    bot: "Bot",
    user_id: int,
    role_id: int,
    resctricted_roles: set[int] | None = None,
) -> None:
    member = bot.guild.get_member(user_id) or await bot.guild.fetch_member(user_id)
    if not member:
        return

    restricted_member_roles = ({role.id for role in member.roles}).intersection(resctricted_roles or set())
    if restricted_member_roles:
        logger.info(
            "Unable to set role #%s for member %s. Restricted roles: %s.",
            role_id,
            member.display_name,
            restricted_member_roles,
        )
        return

    if role := bot.guild.get_role(role_id):
        await member.add_roles(role, reason="ADD_REACTION event")
        logger.info("Set role %s to user %s.", role.name, member.display_name)


async def remove_role(bot: "Bot", user_id: int, role_id: int) -> None:
    member = bot.guild.get_member(user_id) or await bot.guild.fetch_member(user_id)
    if not member:
        return

    if role := bot.guild.get_role(role_id):
        await member.remove_roles(role, reason="ADD_REACTION event")
        logger.info("Removed role %s from user %s.", role.name, member.display_name)


async def schedule_sobriety(
    user: "Member",
    sober_role: "Role",
    mute_seconds: float,
) -> None:
    await asyncio.sleep(mute_seconds)
    await user.remove_roles(sober_role)
    logger.info("%s is now sober.", user.display_name)
    drunkard = await get_drunkard_by_id(user.id)
    if drunkard:
        await user.add_roles(*[user.guild.get_role(role_id) for role_id in drunkard.removed_role_ids])
        logger.info("Set roles %s to user %s", drunkard.removed_role_ids, user.display_name)


@dataclass(frozen=True)
class ScheduledDrunkard:
    member: "Member"
    seconds_left: float


def get_drunk_members(
    all_members: Generator["Member"],
    muted_role: "Role",
    drunkards: dict[int, "Drunkard"],
    current_datetime: datetime,
) -> list[ScheduledDrunkard]:
    """Get members that are drunk with seconds remained to sobriety."""
    drunk_members = []

    for member in all_members:
        if muted_role not in member.roles:
            continue

        user_stat = drunkards.get(member.id)
        if user_stat is None:
            continue

        unmute_date = user_stat.sobriety_date
        seconds_left = 0
        if unmute_date and unmute_date > current_datetime:
            seconds_left = (unmute_date - current_datetime).total_seconds()

        drunk_members.append(ScheduledDrunkard(member=member, seconds_left=seconds_left))

    return drunk_members
