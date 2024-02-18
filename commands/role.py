from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands

from utils.role import parse_roles, parse_categories

if TYPE_CHECKING:
    from bot import EtuUTTBot


# define command group based on the Group class
class Role(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(
            name="role",
            description="Commandes liées à la gestion des rôles (et des salons associés)",
        )

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="getzeroone", description="Affiche les rôles ayant soit 0 ou 1 personne dedans."
    )
    async def get_zero_one(self, interaction: discord.Interaction[EtuUTTBot]):
        await interaction.response.defer(thinking=True)
        counter = 0
        msg = ""
        for role in interaction.guild.roles:
            if len(role.members) <= 1:
                # Arbitrary value to always have messages below 2000 characters (Discord limit)
                if len(msg) > 1600:
                    await interaction.channel.send(msg)
                    msg = ""
                msg += f"- Le rôle {role.name} a {len(role.members)} membres.\n"
                counter += 1
        if counter == 0:
            await interaction.followup.send(
                "\N{WHITE HEAVY CHECK MARK} Commande terminée, aucun rôle n'a été identifié."
            )
            return
        # If at least one role has zero or 1 user in it, there's a list of roles to send
        await interaction.channel.send(msg)
        # Check to send the response to the singular or plural
        if counter == 1:
            await interaction.followup.send(
                "\N{WHITE HEAVY CHECK MARK} Commande terminée, 1 rôle a été identifié :"
            )
            return
        await interaction.followup.send(
            "\N{WHITE HEAVY CHECK MARK} Commande terminée, "
            f"{counter} rôles ont été identifiés :"
        )

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="removeall",
        description="Prend toutes les personnes ayant le rôle et leur retire.",
    )
    async def remove_all(self, interaction: discord.Interaction[EtuUTTBot], role: discord.Role):
        await interaction.response.defer(thinking=True)
        for member in role.members:
            await member.remove_roles(role)
        await interaction.followup.send(
            f"\N{WHITE HEAVY CHECK MARK} Plus personne n'a le rôle {role.name}"
        )

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="addues",
        description="Crée les salons textuels d'un rôle existant. "
                    "La catégorie et le rôle doivent déjà exister.",
    )
    @app_commands.describe(category="La catégorie dans laquelle créer les salons")
    async def add_ues(self, interaction: discord.Interaction[EtuUTTBot], category: str):
        # if len(category) != 19:
        #     await interaction.response.send_message("Ce n'est pas un ID")
        # category = int(category)
        # if category not in (await parse_categories()).keys():
        #     await interaction.response.send_message("Cet ID ne correspond à aucune catégorie.")
        #     return
        # await interaction.response.defer(thinking=True)
        # roles = (await parse_roles("roles.txt")).get(parse_categories().get(category))
        # if roles is None:
        #     await interaction.followup.send("Cette catégorie ne comporte aucune UE.")
        #     return
        await interaction.response.send_message(await parse_roles("roles.txt"))
        await interaction.channel.send(category if not None else "a")

    @add_ues.autocomplete("category")
    async def autocomplete_category(self, interaction: discord.Interaction[EtuUTTBot],
                                    current: str):
        return [app_commands.Choice(name=category, value=category)
                for category in parse_categories().keys() if current.upper() in category.upper()]
