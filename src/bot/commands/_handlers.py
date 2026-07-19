import logging
from typing import TYPE_CHECKING

from .ananaga._help import handle_bot_help
from .ananaga._shots import handle_regular_shot, handle_strong_shot
from .ananaga._statistics import handle_honored_customers, handle_view_stats

if TYPE_CHECKING:
    from discord.ext.commands.context import Context

    from bot import Bot

logger = logging.getLogger(__file__)


def register_commands(bot: "Bot") -> None:
    @bot.command(name='выпил')
    async def regular_shot(ctx: "Context") -> None:
        await handle_regular_shot(bot, ctx)

    @bot.command(name='кончил')
    async def strong_shot(ctx: "Context") -> None:
        await handle_strong_shot(bot, ctx)

    @bot.command(name='лояльность')
    async def view_stats(ctx: "Context") -> None:
        await handle_view_stats(bot, ctx)

    @bot.command(name='рейтинг')
    async def honored_customers(ctx: "Context") -> None:
        await handle_honored_customers(bot, ctx)

    @bot.command(name='помощь')
    async def bot_help(ctx: "Context") -> None:
        await handle_bot_help(bot, ctx)
