from __future__ import annotations

from itertools import groupby
from typing import TYPE_CHECKING

import discord
from discord import CategoryChannel, app_commands

from etuutt_bot.utils.message import split_msg
from etuutt_bot.utils.role import parse_roles

if TYPE_CHECKING:
    from discord import Interaction

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

    @app_commands.command(
        name="lessthan",
        description="Affiche les rôles ayant moins de N personnes dedans (par défaut, n=2).",
    )
    async def get_less_than(self, interaction: discord.Interaction[EtuUTTBot], n: int = 2):
        await interaction.response.defer(thinking=True)
        roles = [r for r in interaction.guild.roles if len(r.members) < n]
        if len(roles) == 0:
            await interaction.followup.send(
                "\N{WHITE HEAVY CHECK MARK} Commande terminée, aucun rôle n'a été identifié."
            )
            return
        if len(roles) == 1:
            await interaction.followup.send(
                "\N{WHITE HEAVY CHECK MARK} Commande terminée, un rôle trouvé : "
                f"{roles[0].name} avec {len(roles[0].members)} membres"
            )
            return
        msg = f"\N{WHITE HEAVY CHECK MARK} Commande terminée, {len(roles)} rôles trouvés : "
        # group roles by ascending number of members
        # start by sorting the roles in order to make the operation
        # O(log(n) + n) instead of O(n²)
        grouped_roles = groupby(
            sorted(roles, key=lambda r: len(r.members)), key=lambda r: len(r.members)
        )
        for nb_members, roles_group in grouped_roles:
            msg += f"\n## Rôles avec {nb_members} membres :\n"
            msg += "\n".join(f"- {r.name}" for r in roles_group)
        chunks = list(split_msg(msg))
        for chunk in chunks[:-1]:
            await interaction.channel.send(chunk)
        # send the last part of the message as a followup
        # to remove the "thinking" message
        await interaction.followup.send(chunks[-1])

    # Remove all users from a role
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    @app_commands.command(
        name="removeall",
        description="Prend toutes les personnes ayant le rôle et leur retire.",
    )
    async def remove_all(self, interaction: Interaction[EtuUTTBot], role: discord.Role):
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
    async def add_ues(self, interaction: Interaction[EtuUTTBot], category: CategoryChannel):
        await interaction.response.defer(thinking=True)
        roles = (await parse_roles("roles.txt")).get(category.name)
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
                lambda r, to_find=role: r.name.upper() == to_find.upper(), interaction.guild.roles
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
                    category=category,
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
