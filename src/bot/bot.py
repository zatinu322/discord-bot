import asyncio
import logging
from collections import defaultdict
from datetime import datetime
from typing import TYPE_CHECKING

from discord import Message
from discord.ext import commands

from bot.commands import register_commands
from bot.events import register_events
from bot.helpers import get_drunk_members, schedule_role_remove, set_role
from bot.messages import handle_multiple_commands
from bot.schemas import ReactionRoleRule
from common_utils import map_drunkards_to_id
from constants.messages import GREETING
from orm.repository.drunkard import get_all_drunkards

if TYPE_CHECKING:
    from shared.config import DiscordSettings

logger = logging.getLogger(__file__)


BOT_NAME = 'PavlikRPG\'s Discord Bot'
BOT_VERSION = '1.1.0'


class Bot(commands.Bot):
    def __init__(self, config: "DiscordSettings", **kwargs):
        super().__init__(**kwargs)

        register_commands(self)
        register_events(self)

        self.config = config

        self.reaction_role_rules = [
            ReactionRoleRule(
                channel_id=config.ENTRANCE.CHANNEL_ID,
                message_id=config.ENTRANCE.MESSAGE_ID,
                emoji=config.ENTRANCE.EMOJI_NAME,
                role_id=config.ENTRANCE.ROLE_ID,
            ),
            ReactionRoleRule(
                channel_id=config.CONTENT.CHANNEL_ID,
                message_id=config.CONTENT.MESSAGE_ID,
                emoji=config.CONTENT.YOUTUBE_EMOJI_NAME,
                role_id=config.CONTENT.YOUTUBE_ROLE_ID,
            ),
            ReactionRoleRule(
                channel_id=config.CONTENT.CHANNEL_ID,
                message_id=config.CONTENT.MESSAGE_ID,
                emoji=config.CONTENT.TWITCH_EMOJI_NAME,
                role_id=config.CONTENT.TWITCH_ROLE_ID,
            ),
        ]
        self.reaction_rules_by_emoji = {rule.emoji: rule for rule in self.reaction_role_rules}

    async def on_ready(self) -> None:
        logger.info('Logged in as %s (ID: %s)', self.user, self.user.id)

        # moved from __init__, because guilds is accessed
        # only after bot logs in
        self.guild = self.get_guild(self.config.SERVER_ID)

        self.drunk_role = self.guild.get_role(self.config.ANANAGA.DRUNK_ROLE_ID)

        self.tavern = self.guild.get_channel(self.config.ANANAGA.TAVERN_CHANNEL_ID)
        self.rehub = self.guild.get_channel(self.config.ANANAGA.REHUB_CHANNEL_ID)

        if self.config.SEND_WELCOME_BAR_MESSAGE:
            await self.tavern.send(GREETING)

        await self.ensure_consistency()

        logger.info('Started %s v%s ', BOT_NAME, BOT_VERSION)

    async def ensure_consistency(self) -> None:
        """Orchestration function, that ensures that:
        - Drunk members has scheduled sobriety.
        - Every member has role provided by added reactions.
        """
        await self.schedule_unmutes()
        await self.ensure_reaction_roles()

    async def ensure_reaction_roles(self) -> None:
        users_by_emoji = defaultdict(set)
        for rule in self.reaction_role_rules:
            channel = self.get_channel(rule.channel_id) or await self.fetch_channel(rule.channel_id)
            message = await channel.fetch_message(rule.message_id)
            for reaction in message.reactions:
                emoji = reaction.emoji.name
                if emoji != rule.emoji:
                    continue
                async for user in reaction.users():
                    users_by_emoji[emoji].add(user.id)

        for rule in self.reaction_role_rules:
            expected_users = users_by_emoji[rule.emoji]
            role = self.guild.get_role(rule.role_id)
            current_users = {member.id for member in role.members}

            for user_id in expected_users - current_users:
                await set_role(self, user_id, rule.role_id)

    async def schedule_unmutes(self) -> None:
        """Get members that are drunk right now."""
        current_datetime = datetime.now()
        drunkards = await get_all_drunkards()
        drunkards_to_id = map_drunkards_to_id(drunkards)

        drunk_members = get_drunk_members(
            all_members=self.get_all_members(),
            muted_role=self.drunk_role,
            drunkards=drunkards_to_id,
            current_datetime=current_datetime,
        )
        tasks = []

        for drunkard in drunk_members:
            member = drunkard.member
            seconds_left = drunkard.seconds_left

            tasks.append(
                    schedule_role_remove(
                    user=member,
                    role=self.drunk_role,
                    mute_seconds=seconds_left,
                ),
            )
            logger.info(
                'Scheduled %s unmute at %s.',
                member.display_name,
                drunkards_to_id[member.id].sobriety_date.strftime("%d/%m/%Y %H:%M"),
            )

        await asyncio.gather(*tasks)

    async def on_message(self, message: "Message") -> None:
        """New messages handler"""
        await handle_multiple_commands(self, message)

    def run(self, **kwargs):
        return super().run(self.config.BOT_TOKEN.get_secret_value(), **kwargs)
