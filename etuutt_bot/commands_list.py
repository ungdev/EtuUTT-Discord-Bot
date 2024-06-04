from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from etuutt_bot.commands.admin import AdminCog
from etuutt_bot.commands.misc import MiscCog
from etuutt_bot.commands.role import RoleCog
from etuutt_bot.commands.ue import UeCog

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot

SPACES = " " * 38


# List of commands to add to the command tree
async def commands_list(bot: EtuUTTBot):
    # Add the cogs to the bot
    # All the cogs are available only on the server which id is given in the config
    for cog in (AdminCog(bot), MiscCog(bot), RoleCog(bot), UeCog(bot)):
        await bot.add_cog(cog, guild=bot.watched_guild)

    # Create a global commands error handler
    @bot.tree.error
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
