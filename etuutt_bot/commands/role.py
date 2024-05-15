from __future__ import annotations

from itertools import groupby
from typing import TYPE_CHECKING

import discord
from discord import Interaction, app_commands
from discord.ext import commands

from etuutt_bot.services.channel import ChannelService
from etuutt_bot.services.role import MergeStrategy, RoleService
from etuutt_bot.utils.message import split_msg

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


@app_commands.default_permissions(administrator=True)
class RoleCog(commands.GroupCog, group_name="role"):
    """Commandes liées à la gestion des rôles"""

    def __init__(self, bot: EtuUTTBot) -> None:
        self.bot = bot
        self.channel_service = ChannelService(bot)
        self.role_service = RoleService(bot)

    @app_commands.command(name="between")
    async def get_roles_with_framed_number_of_members(
        self, interaction: Interaction[EtuUTTBot], nb_min: int = 0, nb_max: int = 1
    ):
        """Affiche les rôles ayant plus de nb_min et moins de nb_max personnes dedans.

        Args:
            interaction:
            nb_min: Le nombre de personnes minimum ayant le rôle (par défaut : 0)
            nb_max: Le nombre de personnes maximum ayant le rôle (par défaut : 1)
        """
        await interaction.response.defer(thinking=True)
        if nb_min > nb_max:
            await interaction.followup.send("Erreur : nb_min doit être inférieur ou égal à nb_max")
            return
        roles = [r for r in interaction.guild.roles if nb_min <= len(r.members) <= nb_max]
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
        for chunk in chunks[1:]:
            await interaction.channel.send(chunk)
        # send the last part of the message as a followup
        # to remove the "thinking" message
        await interaction.followup.send(chunks[0])

    # Remove all users from a role
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    @app_commands.command(name="removeall")
    async def remove_all(self, interaction: Interaction[EtuUTTBot], role: discord.Role):
        """Prend toutes les personnes ayant le rôle et leur retire.

        Args:
            interaction:
            role: le rôle auquel qu'on veut retirer à tout le monde
        """
        await interaction.response.defer(thinking=True)
        for member in role.members:
            await member.remove_roles(role)
        await interaction.followup.send(
            f"\N{WHITE HEAVY CHECK MARK} Plus personne n'a le rôle {role.name}"
        )

    @app_commands.command(name="get_duplicates")
    async def get_duplicates(
        self, interaction: Interaction[EtuUTTBot], case_sensitive: bool = False
    ):
        """Affiche tous les rôles qui sont dupliqués.

        On considère que deux rôles sont dupliqués quand ils ont le même nom.

        Args:
            interaction:
            case_sensitive: La casse est-elle prise en compte dans la recherche des duplications ?
        """
        await interaction.response.defer(thinking=True)
        duplicates = self.role_service.get_duplicates(case_sensitive=case_sensitive)
        if not duplicates:
            await interaction.followup.send("Aucun rôle dupliqué :thumbs_up:")
            return
        message = f"{len(duplicates)} rôles dupliqués :\n"
        message += "\n".join(
            f"- **{d[0].name}**. Nombre de duplications : {len(d)}" for d in duplicates
        )
        await interaction.followup.send(message)

    @app_commands.command(name="merge")
    @app_commands.choices()
    async def merge_roles(
        self,
        interaction: Interaction[EtuUTTBot],
        role: discord.Role,
        case_sensitive: bool = True,
        merge_strategy: MergeStrategy = MergeStrategy.Intersection,
    ):
        """Fusionne en un seul tous les rôles ayant le même nom que le rôle donné.

        Args:
            interaction:
            role: Le rôle qu'on veut fusionner avec tous ceux qui ont le même nom.
            case_sensitive: La casse est-elle prise en compte dans la recherche des duplications ?
            merge_strategy: La manière de fusionner les permissions associées aux rôles fusionnées.

                - Si `Union`, toutes les permissions sont gardées.
                - Si `Intersection`, seules les permissions communes à tous les rôles sont gardées.
                - Si `Clear`, aucune permission n'est gardée.
        """
        await interaction.response.defer(thinking=True)
        duplicates = self.role_service.get_duplicate(role, case_sensitive=case_sensitive)
        nb_duplicates = len(duplicates)
        if nb_duplicates < 2:
            await interaction.followup.send(
                "Ce rôle n'est pas dupliqué :thinking:\n"
                "Utilisez la commande `get_duplicates` pour voir quels rôles sont dupliqués"
            )
            return
        await self.role_service.merge(duplicates, merge_perms_strategy=merge_strategy)
        await interaction.followup.send(
            f"Commande finie. {nb_duplicates} rôles fusionnés. :thumbs_up:"
        )
