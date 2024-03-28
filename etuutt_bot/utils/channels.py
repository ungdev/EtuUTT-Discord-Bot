from __future__ import annotations

from os import getenv
from typing import TYPE_CHECKING

from discord import CategoryChannel, PermissionOverwrite, Role, TextChannel

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


async def create_ue_channel(
    bot: EtuUTTBot, category: CategoryChannel, role: Role, cat: str
) -> TextChannel:
    guild = category.guild
    overwrites = {
        guild.default_role: PermissionOverwrite(read_messages=False),
        role: PermissionOverwrite(read_messages=True),
        guild.get_role(int(getenv("MODERATOR_ID"))): PermissionOverwrite(read_messages=True),
    }
    if elected := bot.data.get("Elected").get(cat):
        overwrites.update({guild.get_role(elected): PermissionOverwrite(read_messages=True)})
    new_channel = await category.create_text_channel(role.name.lower(), overwrites=overwrites)
    await new_channel.send(f"Bonjour {role.mention}, votre salon textuel vient d'être créé !")
    return new_channel
