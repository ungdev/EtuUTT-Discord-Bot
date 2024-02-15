from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands

if TYPE_CHECKING:
    from bot import EtuUTTBot


# define command group based on the Group class
class UE(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(
            name="ue", description="Commandes liées aux UEs (gestion des rôles et des salons)"
        )

    @app_commands.command(
        name="getzeroone", description="Affiche les rôles ayant soit 0 ou 1 personne dedans."
    )
    async def get_zero_one(self, interaction: discord.Interaction[EtuUTTBot]):
        await interaction.response.defer(thinking=True)
        counter = 0
        msg = ""
        for role in interaction.guild.roles:
            if len(role.members) <= 1:
                # Arbitrary value to always have messages below 2000 characters
                if len(msg) > 1600:
                    await interaction.channel.send(msg)
                    msg = ""
                msg += f"- Le rôle {role.name} a {len(role.members)} membres.\n"
                counter += 1
        await interaction.channel.send(msg)
        await interaction.followup.send(
            "\N{WHITE HEAVY CHECK MARK} Commande terminée, "
            f"{counter} rôles ont été identifiés :"
        )
