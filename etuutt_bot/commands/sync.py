from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, app_commands
from discord.ext import commands

from etuutt_bot.services.sync import SyncService

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


@app_commands.default_permissions(administrator=True)
class SyncCog(commands.GroupCog, name="sync"):
    """Commandes liées à la gestion de la synchronisation des rôles."""

    def __init__(self, bot: EtuUTTBot) -> None:
        self.bot = bot
        self.sync_service = SyncService(bot)

    @app_commands.command(name="enable")
    async def sync_enable(self, interaction: Interaction[EtuUTTBot]):
        """Active la synchro automatique."""
        if self.sync_service.is_running():
            await interaction.response.send_message(
                "La synchronisation automatique est déjà activée !"
            )
            return

        self.sync_service.enable_sync()
        await interaction.response.send_message("La synchronisation automatique est activée !")

    @app_commands.command(name="disable")
    async def sync_disable(self, interaction: Interaction[EtuUTTBot]):
        """Désactive la synchro automatique."""
        if not self.sync_service.is_running():
            await interaction.response.send_message(
                "La synchronisation automatique est déjà désactivée !"
            )
            return

        self.sync_service.disable_sync()
        await interaction.response.send_message("La synchronisation automatique est désactivée !")

    @app_commands.command(name="run")
    async def sync_run_once(self, interaction: Interaction[EtuUTTBot]):
        """Éxecute une synchro manuelle."""
        await interaction.response.defer(thinking=True)
        await self.sync_service.run_sync()
        await interaction.followup.send("La synchronisation manuelle est terminée")
