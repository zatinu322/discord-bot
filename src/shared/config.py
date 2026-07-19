from typing import Literal

from pydantic import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DiscordAnanagaSettings(BaseSettings):
    TAVERN_CHANNEL_ID: PositiveInt
    """Bar channel ID."""
    REHUB_CHANNEL_ID: PositiveInt
    """Rehub channel ID."""
    DRUNK_ROLE_ID: PositiveInt
    """Role ID for drunkards."""


class DiscordEntranceSettings(BaseSettings):
    CHANNEL_ID: PositiveInt
    """Channel ID with greeting message."""
    MESSAGE_ID: PositiveInt
    """Server greeting message ID."""
    EMOJI_NAME: str
    """Emoji name for server entrance."""
    ROLE_ID: PositiveInt
    """Role ID for server entrance."""


class DiscordContentSettings(BaseSettings):
    CHANNEL_ID: PositiveInt
    """Channel ID with content roles message."""
    MESSAGE_ID: PositiveInt
    """Message ID for getting content roles."""
    YOUTUBE_EMOJI_NAME: str
    """Emoji name for youtube role."""
    YOUTUBE_ROLE_ID: PositiveInt
    """Youtube role id."""
    TWITCH_EMOJI_NAME: str
    """Emoji name for twitch role."""
    TWITCH_ROLE_ID: PositiveInt
    """Twitch role id."""


class DiscordSettings(BaseSettings):
    BOT_TOKEN: SecretStr
    """Bot token."""
    SERVER_ID: PositiveInt
    """Discord server ID."""
    SEND_WELCOME_BAR_MESSAGE: bool = True
    """Send greeting bar message when bot starts."""

    ANANAGA: DiscordAnanagaSettings
    """Ananaga settings."""
    ENTRANCE: DiscordEntranceSettings
    """Server entrance settings."""
    CONTENT: DiscordContentSettings
    """Content settings."""

    VIP_ROLE_ID: PositiveInt
    """ID роли `Проверенный`."""


class Config(BaseSettings):
    DISCORD: DiscordSettings
    """Discord bot settings."""

    POSTGRES_DSN: SecretStr
    """DSN for Postgres DB."""

    LOG_LEVEL: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    """Logging level."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        validate_default=True,
        extra="forbid",
        use_attribute_docstrings=True,
    )
