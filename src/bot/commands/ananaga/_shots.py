import logging
from datetime import datetime, timedelta
from random import randint
from typing import TYPE_CHECKING

import discord

from bot.helpers import schedule_sobriety
from common_utils import format_time
from constants.messages import (
    BACK_TO_BAR,
    NO_MORE_ANANAGA,
    REGULAR_SHOT,
    STRONG_SHOT,
)
from orm.repository.drunkard import add_shot_to_drunkard

if TYPE_CHECKING:
    from discord import Member, Role
    from discord.ext.commands.context import Context

    from bot import Bot

logger = logging.getLogger(__file__)


async def handle_regular_shot(bot: "Bot", ctx: "Context"):
    if ctx.channel != bot.tavern:
        return

    removed_roles = [bot.entrance_role]
    discord_user = ctx.author
    if bot.vip_role in discord_user.roles:
        removed_roles.append(bot.vip_role)

    mute_seconds = randint(1, 60 * 60 * 24)
    unmute_date: datetime | None = await _add_shot(
        discord_user,
        mute_seconds,
        bot.drunk_role,
        [role.id for role in removed_roles],
    )
    if not unmute_date:
        await ctx.reply(NO_MORE_ANANAGA)
        return

    unmute_date_str = unmute_date.strftime('%d/%m/%Y в %H:%M')
    discord_name = discord_user.display_name
    embed = discord.Embed(
        title=discord_name,
        description=BACK_TO_BAR,
    )
    embed.set_footer(text=unmute_date_str)

    await ctx.reply(
        REGULAR_SHOT.format(
            discord_name=discord_name,
            mute_seconds=format_time(mute_seconds),
        ),
        mention_author=True,
        embed=embed,
    )
    await discord_user.add_roles(bot.drunk_role)
    await discord_user.remove_roles(*removed_roles)
    logger.info('%s is drunk until %s.', discord_name, unmute_date_str)

    await schedule_sobriety(discord_user, bot.drunk_role, mute_seconds)


async def handle_strong_shot(bot: "Bot", ctx: "Context"):
    if ctx.channel != bot.tavern:
        return

    removed_roles = [bot.entrance_role]
    discord_user = ctx.author
    if bot.vip_role in discord_user.roles:
        removed_roles.append(bot.vip_role)

    mute_seconds = 60 * 60 * 24 * 2
    unmute_date = await _add_shot(
        discord_user,
        mute_seconds,
        bot.drunk_role,
        [role.id for role in removed_roles],
    )
    if not unmute_date:
        await ctx.reply(NO_MORE_ANANAGA)
        return

    unmute_date_str = unmute_date.strftime('%d/%m/%Y в %H:%M')
    discord_name = discord_user.display_name
    embed = discord.Embed(
        title=discord_name,
        description=BACK_TO_BAR,
    )
    embed.set_footer(text=unmute_date_str)

    await ctx.reply(
        STRONG_SHOT.format(
            discord_name=discord_name,
            mute_seconds=format_time(mute_seconds),
        ),
        mention_author=True,
        embed=embed,
    )

    await discord_user.add_roles(bot.drunk_role)
    await discord_user.remove_roles(*removed_roles)
    logger.info('%s is drunk until %s.', discord_name, unmute_date_str)

    await schedule_sobriety(discord_user, bot.drunk_role, mute_seconds)


async def _add_shot(
    discord_user: "Member",
    mute_seconds: int,
    muted_role: "Role",
    removed_role_ids: list[int],
) -> datetime | None:
    if muted_role in discord_user.roles:
        return None

    unmute_date = datetime.now() + timedelta(seconds=mute_seconds)
    await add_shot_to_drunkard(
        drunkard_id=discord_user.id,
        drunk_time=mute_seconds,
        unmute_date=unmute_date,
        removed_role_ids=removed_role_ids,
    )

    return unmute_date
