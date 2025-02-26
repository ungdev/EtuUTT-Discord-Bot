from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class AdminCog(commands.Cog):
    """Commandes pour les administrateurs du bot."""

    def __init__(self, bot: EtuUTTBot) -> None:
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="sync")
    async def sync_tree(self, ctx: commands.Context[EtuUTTBot]):
        """Commande pour synchroniser les commandes slash du bot.

        Reservée au propriétaire et aux membres de l'équipe du bot.
        """
        try:
            await self.bot.tree.sync()
            for guild in self.bot.guilds:
                await self.bot.tree.sync(guild=guild)
            await ctx.reply("Les commandes slash ont bien été synchronisées.")
        except discord.app_commands.CommandSyncFailure as e:
            self.bot.logger.error(e)
            await ctx.reply(
                f"Il y a eu une erreur lors de la synchronisation des commandes slash\n{e}"
            )

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[EtuUTTBot], error: commands.CommandError
    ):
        """Gestionnaire d'erreur des commandes de la classe."""
        if isinstance(error, commands.NotOwner):
            self.bot.logger.info(f"{ctx.author}, who isn't authorized, tried to sync the commands")
            return
        self.bot.logger.info(error)
