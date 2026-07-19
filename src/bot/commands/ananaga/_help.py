from typing import TYPE_CHECKING

from constants.messages import HELP_MESSAGE

if TYPE_CHECKING:
    from discord.ext.commands.context import Context

    from bot import Bot


async def handle_bot_help(bot: "Bot", ctx: "Context"):
    if ctx.channel != bot.tavern:
        return

    await ctx.reply(HELP_MESSAGE)
