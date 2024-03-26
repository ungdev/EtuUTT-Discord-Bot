from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class Misc(commands.Cog):
    def __init__(self, bot: EtuUTTBot) -> None:
        self.bot = bot
        # Circumvent impossibility to add context menu commands in cogs
        self.ctx_pin = app_commands.ContextMenu(
            name="Épingler/Désépingler",
            callback=self.pin,
        )
        self.ctx_delete = app_commands.ContextMenu(
            name="Supprimer jusqu'ici",
            callback=self.delete,
        )
        self.bot.tree.add_command(self.ctx_pin)
        self.bot.tree.add_command(self.ctx_delete)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_pin.name, type=self.ctx_pin.type)
        self.bot.tree.remove_command(self.ctx_delete.name, type=self.ctx_delete.type)

    # Simple ping command
    @app_commands.command(name="ping", description="Teste le ping du bot")
    async def ping(self, interaction: discord.Interaction[EtuUTTBot]):
        await interaction.response.send_message(
            f"Pong! En {round(interaction.client.latency * 1000)}ms"
        )

    # Make a simple context menu application to pin/unpin
    @app_commands.guild_only
    @app_commands.default_permissions(send_messages=True)
    @app_commands.checks.has_permissions(send_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def pin(self, interaction: discord.Interaction[EtuUTTBot], message: discord.Message):
        if message.pinned:
            await message.unpin()
            await interaction.response.send_message(
                "Le message a été désépinglé !", ephemeral=True
            )
        else:
            await message.pin()
            await interaction.response.send_message("Le message a été épinglé !", ephemeral=True)

    # Make a context menu command to delete messages
    @app_commands.guild_only
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(
        manage_messages=True, read_message_history=True, read_messages=True
    )
    async def delete(self, interaction: discord.Interaction[EtuUTTBot], message: discord.Message):
        await interaction.response.defer(ephemeral=True, thinking=True)
        last_id = interaction.channel.last_message_id

        def is_msg(msg: discord.Message) -> bool:
            return (message.id >> 22) <= (msg.id >> 22) <= (last_id >> 22)

        del_msg = await message.channel.purge(
            bulk=True, reason="Admin used bulk delete", check=is_msg
        )
        await interaction.followup.send(f"{len(del_msg)} messages supprimés !")
