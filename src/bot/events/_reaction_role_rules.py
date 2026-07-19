from typing import TYPE_CHECKING

from bot.schemas import ReactionRoleRule

if TYPE_CHECKING:
    from shared.config import DiscordSettings


def get_reaction_role_rules(config: "DiscordSettings") -> list[ReactionRoleRule]:
    return [
        ReactionRoleRule(
            channel_id=config.ENTRANCE.CHANNEL_ID,
            message_id=config.ENTRANCE.MESSAGE_ID,
            emoji=config.ENTRANCE.EMOJI_NAME,
            role_id=config.ENTRANCE.ROLE_ID,
            restricted_roles={config.ANANAGA.DRUNK_ROLE_ID},
        ),
        ReactionRoleRule(
            channel_id=config.CONTENT.CHANNEL_ID,
            message_id=config.CONTENT.MESSAGE_ID,
            emoji=config.CONTENT.YOUTUBE_EMOJI_NAME,
            role_id=config.CONTENT.YOUTUBE_ROLE_ID,
            restricted_roles=set(),
        ),
        ReactionRoleRule(
            channel_id=config.CONTENT.CHANNEL_ID,
            message_id=config.CONTENT.MESSAGE_ID,
            emoji=config.CONTENT.TWITCH_EMOJI_NAME,
            role_id=config.CONTENT.TWITCH_ROLE_ID,
            restricted_roles=set(),
        ),
    ]
