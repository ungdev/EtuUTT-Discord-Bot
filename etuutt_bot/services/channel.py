from __future__ import annotations

from typing import TYPE_CHECKING

from discord import (
    CategoryChannel,
    ForumChannel,
    StageChannel,
    TextChannel,
    VoiceChannel,
)

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot

type AnyChannel = VoiceChannel | StageChannel | ForumChannel | TextChannel | CategoryChannel


class ChannelService:
    def __init__(self, bot: EtuUTTBot):
        self._bot = bot

    def find_by_name(
        self, name: str, *, channel_type: type[AnyChannel] | None = None
    ) -> AnyChannel | None:
        name = name.lower()
        channels = self._bot.watched_guild.channels
        if channel_type:
            channels = (c for c in channels if isinstance(c, channel_type))
        return next((c for c in channels if c.name == name), None)
