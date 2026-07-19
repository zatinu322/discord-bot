import logging

import discord

from bot import Bot
from shared.app_context import get_config

logger = logging.getLogger(__file__)
config = get_config()


def main() -> None:
    logging.basicConfig(
        format='[%(levelname)s - %(asctime)s - %(name)s]: %(message)s',
        level=config.LOG_LEVEL,
        datefmt='%Y-%m-%d-%H:%M:%S',
    )

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    discord_bot = Bot(
        config=config.DISCORD,
        command_prefix='!',
        intents=intents,
        case_insensitive=True,
    )
    discord_bot.run()


if __name__ == '__main__':
    main()
