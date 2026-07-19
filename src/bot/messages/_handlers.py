import logging
from typing import TYPE_CHECKING

from constants.messages import MORE_THAN_ONE_COMMAND

if TYPE_CHECKING:
    from discord import Message

    from bot import Bot

logger = logging.getLogger(__file__)


async def handle_multiple_commands(bot: "Bot", message: "Message"):
    if message.author == bot.user:
        return

    if message.channel not in {bot.tavern, bot.rehub}:
        return

    total_commands = 0
    requested_command = None
    message_words = message.content.lower().split()

    for command in bot.commands:
        command_str = f'{bot.command_prefix}{command.name}'
        if command_str in message_words:
            total_commands += 1
            requested_command = command_str

    ctx = await bot.get_context(message)

    if total_commands == 1:
        message.content = requested_command
        ctx = await bot.get_context(message)
        await bot.invoke(ctx)
    elif total_commands > 1:
        await ctx.reply(MORE_THAN_ONE_COMMAND, mention_author=True)
