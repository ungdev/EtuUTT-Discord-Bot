from os import getenv

from discord import CategoryChannel, PermissionOverwrite, Role, TextChannel


async def create_ue_channel(
    category: CategoryChannel, role: Role, elected: Role = None
) -> TextChannel:
    guild = category.guild
    overwrites = {
        guild.default_role: PermissionOverwrite(read_messages=False),
        role: PermissionOverwrite(read_messages=True),
        guild.get_role(int(getenv("MODERATOR_ID"))): PermissionOverwrite(read_messages=True),
    }
    if elected:
        overwrites.update({elected: PermissionOverwrite(read_messages=True)})
    new_channel = await category.create_text_channel(role.name.lower(), overwrites=overwrites)
    await new_channel.send(f"Bonjour {role.mention}, votre salon textuel vient d'être créé !")
    return new_channel
