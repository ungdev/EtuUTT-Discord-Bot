from __future__ import annotations

from typing import TYPE_CHECKING

from discord import CategoryChannel, Interaction, TextChannel, app_commands
from discord.ext import commands

from etuutt_bot.services.ue import (
    AlreadyExistsError,
    CategoryMissingError,
    MissingConfigurationError,
    UeService,
)
from etuutt_bot.utils.message import split_msg

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


@app_commands.default_permissions(administrator=True)
class UeCog(commands.GroupCog, group_name="ues"):
    """Commandes liées à la gestion des UEs."""

    def __init__(self, bot: EtuUTTBot):
        self.bot = bot
        self.ue_service = UeService(bot)

    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    @app_commands.command(name="add_all")
    async def add_category(self, interaction: Interaction[EtuUTTBot], category: CategoryChannel):
        """Crée les salons textuels et les rôles pour toutes les UEs d'une catégorie.

        Args:
            interaction:
            category: La catégorie dans laquelle on veut créer les salons d'UE
        """
        await interaction.response.defer(thinking=True)
        settings_cat = next(
            (cat for cat in self.bot.settings.categories if cat.id == category.id), None
        )
        if settings_cat is None:
            await interaction.followup.send(
                f"La catégorie {category.name} n'est pas destinée à accueillir des salons d'UE"
            )
            return
        ues_names = {ue.lower() for ue in settings_cat.ues}
        msg = ""

        # Ensure that channels don't exist yet in order not to overwrite them
        to_create = self.ue_service.get_missing_channels(category)
        if len(to_create) < len(settings_cat.ues):
            msg += "\n## \N{SLEEPING SYMBOL} Les salons suivants existent déjà :\n"
            msg += "\n".join(f"- {c}" for c in ues_names - to_create)

        if len(to_create) > 0:
            msg += "\n## Salons textuels créés :\n"
            for channel_name in to_create:
                channel, role = await self.ue_service.create_channel(channel_name)
                await channel.send(
                    f"{role.mention} votre salon vient d'être créé \N{WAVING HAND SIGN}"
                )
                msg += f"\n- {channel.name}"

        for chunk in split_msg(msg):
            await interaction.channel.send(chunk)
        await interaction.followup.send("\N{WHITE HEAVY CHECK MARK} La commande est terminée :")

    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    @app_commands.command(name="add")
    async def add_one(self, interaction: Interaction[EtuUTTBot], ue: str):
        """Crée le salon correspondant à l'UE donnée.

        Args:
            interaction:
            ue: le nom de l'UE à créer
        """
        await interaction.response.defer(thinking=True)
        try:
            channel, role = await self.ue_service.create_channel(ue)
        except AlreadyExistsError:
            await interaction.followup.send("Ce salon existe déjà.")
            return
        except MissingConfigurationError:
            await interaction.followup.send(
                "Cette UE n'a pas été trouvée dans la configuration du bot.\n"
                "Vous avez peut-être fait une faute de frappe, "
                "ou bien la configuration du bot n'est pas à jour avec le catalogue des UEs."
            )
            return
        except CategoryMissingError:
            await interaction.followup.send(
                "La catégorie pour cette UE n'existe pas "
                "ou l'ID est incorrect dans la configuration."
            )
            return
        await channel.send(f"{role.mention} votre salon vient d'être créé \N{WAVING HAND SIGN}")
        await interaction.followup.send("Salon créé \N{THUMBS UP SIGN}")

    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    @app_commands.command(name="remove_all")
    async def delete_many(
        self,
        interaction: Interaction[EtuUTTBot],
        category: CategoryChannel,
        delete_roles: bool = True,
    ):
        """Supprime les salons de toutes les UEs de la catégorie donnée.

        Args:
            category: la catégorie dans laquelle supprimer tous les salons d'UE
            delete_roles: si `True`, les rôles associés aux UEs sont également supprimés
        """
        await interaction.response.defer(thinking=True)
        nb_deleted = await self.ue_service.delete_all_channels(category, delete_roles=delete_roles)
        await interaction.followup.send(f"Commande finie. {nb_deleted} salons supprimés.")

    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    @app_commands.command(name="remove")
    async def delete_one(
        self,
        interaction: Interaction[EtuUTTBot],
        channel: TextChannel,
        delete_role: bool = True,
    ):
        """Supprime le salon d'UE donné.

        Args:
            channel: le salon d'UE à supprimer
            delete_role: si `True`, le rôle associé à l'UE sont également supprimés
        """
        await interaction.response.defer(thinking=True)
        await self.ue_service.delete_channel(channel, delete_role=delete_role)
        await interaction.followup.send("Commande finie. Salon supprimé.")

    @add_one.autocomplete("ue")
    async def autocomplete_missing_ue(self, interaction: Interaction[EtuUTTBot], current: str):
        """Autocomplétion pour les ues dont le salon n'existe pas.

        Comme le but de cette autocomplétion est de suggérer
        des noms de salons qui n'ont *pas encore* été créés et pour
        lesquels il n'existe *pas encore* forcément de rôle,
        on ne peut pas utiliser les fonctions d'autocomplétion par défaut.
        """
        ues = self.ue_service.get_missing_channels()
        return [app_commands.Choice(name=ue, value=ue) for ue in ues if current.lower() in ue]
