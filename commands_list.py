from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from commands.misc import ping, pin, delete
from commands.ue import UE

if TYPE_CHECKING:
    from bot import EtuUTTBot

# List the commands and commands groups
COMMANDS_LIST: tuple = (ping, pin, delete, UE())

SPACES = " " * 38


# List of commands to add to the command tree
async def commands(tree: discord.app_commands.CommandTree):
    # Add the commands to the Tree
    for command in COMMANDS_LIST:
        tree.add_command(command)

    # Create a global commands error handler
    @tree.error
    async def on_command_error(
        interaction: discord.Interaction[EtuUTTBot], error: discord.app_commands.AppCommandError
    ):
        # The bot is missing permissions
        if isinstance(error, discord.app_commands.BotMissingPermissions):
            bot_perms = ", ".join(error.missing_permissions)
            interaction.client.logger.error(
                f"{interaction.client.user} is missing {bot_perms} "
                f"to do {interaction.command.name} in #{interaction.channel}"
            )
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(
                    f"Il me manque cette permission : {bot_perms}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"Il me manque ces permissions : {bot_perms}",
                    ephemeral=True,
                )
            return
        # The user is missing permissions
        if isinstance(error, discord.app_commands.MissingPermissions):
            user_perms = ", ".join(error.missing_permissions)
            interaction.client.logger.error(
                f"{interaction.user} is missing {user_perms} "
                f"to do {interaction.command.name} in #{interaction.channel}"
            )
            if len(error.missing_permissions) == 1:
                await interaction.response.send_message(
                    f"Il te manque cette permission : {user_perms}",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"Il te manque ces permissions : {user_perms}",
                    ephemeral=True,
                )
            return
        # Other errors with a check decorator
        if isinstance(error, discord.app_commands.CheckFailure):
            interaction.client.logger.error(
                f"{interaction.user} tried to do {interaction.command.name} "
                f"in #{interaction.channel}\n{SPACES}{error}"
            )
            await interaction.response.send_message(
                "Tu n'as pas le droit d'utiliser cette commande !",
                ephemeral=True,
            )
            return
        # Other errors
        interaction.client.logger.error(error)
        await interaction.response.send_message(
            f"{error}\nCette erreur n'est pas gérée, signalez-la !"
        )
