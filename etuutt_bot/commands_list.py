from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from etuutt_bot.commands.admin import AdminCog
from etuutt_bot.commands.anon_msg import AnonMsgCog
from etuutt_bot.commands.config import ConfigCog
from etuutt_bot.commands.misc import MiscCog
from etuutt_bot.commands.role import RoleCog
from etuutt_bot.commands.sync import SyncCog

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot

SPACES = " " * 38


async def commands_list(bot: EtuUTTBot):
    """Liste les cogs et les ajoute au bot."""
    # Les cogs contenant les commandes globales
    global_cogs: tuple = (AdminCog(bot), MiscCog(bot))
    for cog in global_cogs:
        await bot.add_cog(cog)

    # Les cogs contenant les commandes réservées à la guilde gérée
    guild_cogs: tuple = (AnonMsgCog(bot), ConfigCog(bot), RoleCog(bot), SyncCog(bot))
    for cog in guild_cogs:
        await bot.add_cog(cog, guild=bot.watched_guild)

    # Gestionnaire d'erreurs des commandes
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
