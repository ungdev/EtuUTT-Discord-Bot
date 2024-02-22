from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from src.bot import EtuUTTBot


class Admin(commands.Cog):
    # Add command to sync slash commands for team members and owner of the bot
    @commands.is_owner()
    @commands.command(name="sync")
    async def sync_tree(self, ctx: commands.Context[EtuUTTBot]):
        try:
            await ctx.bot.tree.sync()
            for guild in ctx.bot.guilds:
                await ctx.bot.tree.sync(guild=guild)
            await ctx.reply("Les commandes slash ont bien été synchronisées.")
        except discord.app_commands.CommandSyncFailure as e:
            ctx.bot.logger.error(e)
            await ctx.reply(
                f"Il y a eu une erreur lors de la synchronisation des commandes slash\n{e}"
            )
        return

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context[EtuUTTBot], error: commands.CommandError
    ):
        if isinstance(error, commands.NotOwner):
            ctx.bot.logger.info(f"{ctx.author}, who isn't authorized, tried to sync the commands")
            return
        ctx.bot.logger.info(error)
