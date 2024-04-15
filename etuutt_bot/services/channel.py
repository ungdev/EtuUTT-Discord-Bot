from __future__ import annotations

from typing import TYPE_CHECKING

from discord import CategoryChannel, PermissionOverwrite, Role, TextChannel

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class ChannelService:
    def __init__(self, bot: EtuUTTBot):
        self._bot = bot

    async def create_ue_channel(
        self, category: CategoryChannel, role: Role, elected: Role | None = None
    ) -> TextChannel:
        guild = category.guild
        moderator_role = guild.get_role(self._bot.settings.guild.special_roles.moderator)
        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            role: PermissionOverwrite(read_messages=True),
            moderator_role: PermissionOverwrite(read_messages=True),
        }
        if elected:
            overwrites[elected] = PermissionOverwrite(read_messages=True)
        new_channel = await category.create_text_channel(role.name.lower(), overwrites=overwrites)
        await new_channel.send(f"Bonjour {role.mention}, votre salon textuel vient d'être créé !")
        return new_channel
