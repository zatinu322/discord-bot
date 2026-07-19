import logging
from typing import TYPE_CHECKING

import discord
from discord import Embed

from common_utils import format_time, get_correct_count_spelling
from constants.messages import HONORED_DRUNKARDS, NO_RECORD, USER_STAT
from orm.repository.drunkard import get_all_drunkards, get_drunkard_by_id

if TYPE_CHECKING:
    from discord.ext.commands.context import Context

    from bot import Bot

logger = logging.getLogger(__file__)


async def handle_view_stats(bot: "Bot", ctx: "Context") -> None:
    if ctx.channel not in {bot.tavern, bot.rehub}:
        return

    discord_user = ctx.author
    drunkard = await get_drunkard_by_id(discord_user.id)
    if not drunkard:
        await ctx.reply(
            NO_RECORD,
            mention_author=True)
        return

    emb = discord.Embed(
        title=discord_user.display_name,
        description=USER_STAT.format(
            shots_count=drunkard.shots_count,
            drunk_time=format_time(drunkard.drunk_time),
        ),
    )
    await ctx.reply(embed=emb, mention_author=True)


async def handle_honored_customers(bot: "Bot", ctx: "Context") -> None:
    if ctx.channel not in {bot.tavern, bot.rehub}:
        return

    discord_names_to_id = {member.id: member.display_name for member in bot.get_all_members()}
    # FIXME: What if user is not on server?

    drunkards = await get_all_drunkards()
    longest_drunkards = sorted(drunkards, key=lambda drunkard: drunkard.drunk_time, reverse=True)
    fastest_drunkards = sorted(drunkards, key=lambda drunkard: drunkard.shots_count, reverse=True)

    honored_drunkards_str = HONORED_DRUNKARDS.format(
        longest_drunkards="\n".join(
            [
                f"- {discord_names_to_id.get(drunkard.id)}:\n  {drunkard.drunk_time} секунд"
                for drunkard in longest_drunkards[:5]
            ],
        ),
        fastest_drunkards="\n".join(
            [
                f"- {discord_names_to_id.get(drunkard.id)}:\n  {drunkard.shots_count} "
                f"{get_correct_count_spelling(drunkard.shots_count)}"
                for drunkard in fastest_drunkards[:5]
            ],
        ),
    )

    emb = Embed(description=honored_drunkards_str)
    await ctx.reply(embed=emb, mention_author=True)
