from discord import CategoryChannel, PermissionOverwrite, Role, TextChannel


async def create_ue_channel(category: CategoryChannel, role: Role) -> TextChannel:
    default_role = category.guild.default_role
    new_channel = await category.create_text_channel(
        role.name.lower(),
        overwrites={
            default_role: PermissionOverwrite(read_messages=False),
            role: PermissionOverwrite(read_messages=True),
        },
    )
    await new_channel.send(f"Bonjour {role.mention}, votre salon textuel vient d'être créé !")
    return new_channel
