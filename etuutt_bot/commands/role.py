from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands

from etuutt_bot.utils.role import parse_categories, parse_roles

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


# define command group based on the Group class
class Role(app_commands.Group):
    # Set command group name and description
    def __init__(self):
        super().__init__(
            name="role",
            description="Commandes liées à la gestion des rôles (et des salons associés)",
            default_permissions=discord.Permissions(administrator=True),
        )

    # Check the roles with 0 or 1 user in it
    @app_commands.command(
        name="getzeroone", description="Affiche les rôles ayant soit 0 ou 1 personne dedans."
    )
    async def get_zero_one(self, interaction: discord.Interaction[EtuUTTBot]):
        # TODO refaire en afficher les rôles avec x personnes ou moins dedans
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

    # Remove all users from a role
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
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

    # define sub command group to manage channels
    channel = app_commands.Group(
        name="channel",
        description="Commandes liées à la gestion des salons associés aux rôles",
    )

    # Create the channels for all courses in a specified category
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @channel.command(
        name="addall",
        description="Crée les salons textuels d'un rôle existant. "
        "La catégorie et le rôle doivent déjà exister.",
    )
    @app_commands.describe(category="La catégorie dans laquelle créer les salons")
    async def add_ues(self, interaction: discord.Interaction[EtuUTTBot], category: str):
        if category not in parse_categories():
            await interaction.response.send_message("Cet ID ne correspond à aucune catégorie.")
            return
        await interaction.response.defer(thinking=True)
        roles = (await parse_roles("roles.txt")).get(category)
        if roles is None:
            await interaction.followup.send("Cette catégorie ne comporte aucune UE.")
            return
        msg = ""
        for role in roles:
            # Arbitrary value to always have messages below 2000 characters (Discord limit)
            if len(msg) > 1600:
                await interaction.channel.send(msg)
                msg = ""
            role_d = discord.utils.find(
                lambda r: r.name.upper() == role.upper(),
                interaction.guild.roles,  # noqa B023
            )
            if role_d is None:
                msg += f"\N{WHITE QUESTION MARK ORNAMENT} Pas de rôle pour {role}\n"
                continue
            if any(c.name.upper() == role.upper() for c in interaction.guild.channels):
                msg += f"\N{SLEEPING SYMBOL} Le salon textuel {role.lower()} existe déjà\n"
                continue
            await (
                await interaction.guild.create_text_channel(
                    role.lower(),
                    category=interaction.guild.get_channel(parse_categories().get(category)),
                    overwrites={
                        interaction.guild.default_role: discord.PermissionOverwrite(
                            read_messages=False
                        ),
                        role_d: discord.PermissionOverwrite(read_messages=True),
                    },
                )
            ).send(f"Bonjour {role_d.mention}, votre salon textuel vient d'être créé !")
            msg += f"\N{WHITE HEAVY CHECK MARK} Le salon {role.lower()} a été créé\n"
        await interaction.channel.send(msg)
        await interaction.followup.send("\N{WHITE HEAVY CHECK MARK} La commande est terminée :")

    # Autocomplete the category
    @add_ues.autocomplete("category")
    async def autocomplete_category(
        self, interaction: discord.Interaction[EtuUTTBot], current: str
    ):
        return [
            app_commands.Choice(name=category, value=category)
            for category in parse_categories()
            if current.upper() in category
        ]
