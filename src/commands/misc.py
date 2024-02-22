from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands

if TYPE_CHECKING:
    from src.bot import EtuUTTBot


# Simple ping command
@app_commands.command(name="ping", description="Teste le ping du bot")
async def ping(interaction: discord.Interaction[EtuUTTBot]):
    await interaction.response.send_message(
        f"Pong! En {round(interaction.client.latency * 1000)}ms"
    )


# Make a simple context menu application to pin/unpin
@app_commands.guild_only
@app_commands.default_permissions(send_messages=True)
@app_commands.checks.has_permissions(send_messages=True)
@app_commands.checks.bot_has_permissions(manage_messages=True)
@app_commands.context_menu(name="Épingler/Désépingler")
async def pin(interaction: discord.Interaction[EtuUTTBot], message: discord.Message):
    if message.pinned:
        await message.unpin()
        await interaction.response.send_message("Le message a été désépinglé !", ephemeral=True)
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
@app_commands.context_menu(name="Supprimer jusqu'ici")
async def delete(interaction: discord.Interaction[EtuUTTBot], message: discord.Message):
    await interaction.response.defer(ephemeral=True, thinking=True)
    last_id = interaction.channel.last_message_id

    def is_msg(msg: discord.Message) -> bool:
        return (message.id >> 22) <= (msg.id >> 22) <= (last_id >> 22)

    del_msg = await message.channel.purge(bulk=True, reason="Admin used bulk delete", check=is_msg)
    await interaction.followup.send(f"{len(del_msg)} messages supprimés !")
