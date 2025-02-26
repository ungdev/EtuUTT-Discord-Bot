from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from discord import Interaction, TextChannel, app_commands
from discord.ext import commands

from etuutt_bot.utils.data_write import data_write

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class AnonMsgCog(commands.GroupCog, group_name="anon"):
    """Commandes pour envoyer des messages anonymes."""

    def __init__(self, bot: EtuUTTBot):
        self.bot = bot

    @app_commands.command(name="send")
    @app_commands.rename(channel="salon")
    async def send(self, interaction: Interaction[EtuUTTBot], channel: TextChannel, message: str):
        """Envoie un message anonyme dans le salon demandé s'il le supporte."""
        if channel.id not in self.bot.settings.guild.anonymous_channels:
            await interaction.response.send_message(
                "Le salon ne supporte pas les messages anonymes"
            )
            return
        msg = await channel.send(f"[ANONYME] {message}")
        await data_write(
            f"[{datetime.now().isoformat(' ', 'seconds')}]"
            f" {interaction.user.name} alias {interaction.user.display_name}"
            f" a envoyé le message {msg.id} sur le salon #{channel.name}.\n",
            Path("data", "logs", "anon.log"),
        )
        await interaction.response.send_message(
            f"Votre message a bien été envoyé : {msg.jump_url}", ephemeral=True
        )

    @app_commands.command(name="liste")
    async def list(self, interaction: Interaction[EtuUTTBot]):
        """Envoie la liste des salons dans lesquels un message anonyme peut être envoyé."""
        if not self.bot.settings.guild.anonymous_channels:
            await interaction.response.send_message(
                "Il n'y a pas de salon configuré pour envoyer un message anonyme."
            )
        msg = "Les salons dans lesquels un message anonyme peut être envoyé sont :"
        for c in self.bot.settings.guild.anonymous_channels:
            msg += f"\n- {interaction.guild.get_channel(c).mention}"
        await interaction.response.send_message(msg)
