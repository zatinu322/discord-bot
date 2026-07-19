import logging
from typing import TYPE_CHECKING

from ._role_manager import handle_raw_reaction_add, handle_raw_reaction_remove

if TYPE_CHECKING:
    from discord import RawReactionActionEvent

    from bot import Bot

logger = logging.getLogger(__file__)


def register_events(bot: "Bot") -> None:
    @bot.event
    async def on_raw_reaction_add(payload: "RawReactionActionEvent"):
        await handle_raw_reaction_add(bot, payload)

    @bot.event
    async def on_raw_reaction_remove(payload: "RawReactionActionEvent"):
        await handle_raw_reaction_remove(bot, payload)
