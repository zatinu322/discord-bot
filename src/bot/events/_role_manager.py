import logging
from typing import TYPE_CHECKING

from bot.helpers import remove_role, set_role

if TYPE_CHECKING:
    from discord import RawReactionActionEvent

    from bot import Bot

logger = logging.getLogger(__file__)


async def handle_raw_reaction_add(bot: "Bot", payload: "RawReactionActionEvent") -> None:
    if payload.user_id == bot.user.id:
        return

    rule = bot.reaction_rules_by_emoji.get(payload.emoji.name)
    if not rule:
        return

    if payload.message_id != rule.message_id:
        return

    await set_role(bot, payload.user_id, rule.role_id)


async def handle_raw_reaction_remove(bot: "Bot", payload: "RawReactionActionEvent") -> None:
    if payload.user_id == bot.user.id:
        return

    rule = bot.reaction_rules_by_emoji.get(payload.emoji.name)
    if not rule:
        return

    if payload.message_id != rule.message_id:
        return

    await remove_role(bot, payload.user_id, rule.role_id)
