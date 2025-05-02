from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import Interaction, app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


@app_commands.default_permissions(administrator=True)
class ConfigCog(commands.GroupCog, name="config"):
    """Commandes liées à la gestion de la configuration du bot."""

    def __init__(self, bot: EtuUTTBot) -> None:
        self.bot = bot

    @app_commands.command(name="download")
    async def config_download(self, interaction: Interaction[EtuUTTBot]) -> None:
        """Permet de télécharger la configuration actuelle du bot."""
        await interaction.response.send_message(
            file=discord.File(self.bot.config_file), ephemeral=True
        )

    @app_commands.command(name="upload")
    async def config_upload(
        self, interaction: Interaction[EtuUTTBot], file: discord.Attachment
    ) -> None:
        """Permet de téléverser une nouvelle configuration puis de redémarrer le bot pour la charger."""
        if (file.filename != "discord.toml") or ("text" not in file.content_type):
            await interaction.response.send_message(
                "Le fichier fourni ne s'appelle pas `discord.toml` ou ne contient pas de texte.",
                ephemeral=True,
            )
            return
        self.bot.config_file.replace(self.bot.backup_config_file)
        await file.save(self.bot.config_file)
        await self.bot.watched_guild.get_channel(self.bot.settings.guild.channel_admin_id).send(
            f"Une nouvelle configuration a été chargée par {interaction.user.name}."
        )
        await interaction.response.send_message(
            "La configuration a bien été chargée, je vais redémarrer.", ephemeral=True
        )
        await self.bot.close()
