from __future__ import annotations

from typing import TYPE_CHECKING

from discord import CategoryChannel, PermissionOverwrite, Role, TextChannel

from etuutt_bot.types import LowerStr

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class MissingConfigurationError(Exception):
    """On a recherché un élément qui n'est pas renseigné dans la configuration."""


class AlreadyExistsError(Exception):
    """On a tenté de créer un élément qui existe déjà."""


class UeService:
    """Service de gestion des UEs, avec leurs rôles, salons et catégories.

    Warning:
        Faire correspondre les noms des UEs tels qu'ils peuvent apparaitre
        dans la configuration, les noms des rôles et les noms des salons,
        peut demander une certaine gymnastique entre majuscules et minuscules.

        C'est pourquoi il est important de garder en tête les conventions suivantes :

        - les noms dans la configuration sont en majuscules (GE21, MATH01, PHYS11...)
        - les noms des rôles sont en majuscules (GE21, MATH01, PHYS11...)
        - les noms des salons sont en minuscules (ge21, math01, phys11...)
        - les noms des catégories sont en majuscules (ME, CS, TM...)
    """

    def __init__(self, bot: EtuUTTBot):
        self._bot = bot

    @staticmethod
    async def delete_channel(channel: TextChannel, *, delete_role: bool = False) -> None:
        """Supprime un salon d'UE.

        Args:
            channel: Le salon à supprimer
            delete_role: si `True`, supprime également le rôle associé à l'UE
        """
        if delete_role:
            ue_role = next(
                (r for r in channel.guild.roles if r.name.lower() == channel.name),
                None,
            )
            if ue_role is not None:
                await ue_role.delete(reason="Suppression du rôle associé à un salon d'UE")
        await channel.delete(reason="Suppression d'un salon d'UE")

    async def delete_all_channels(
        self, category: CategoryChannel, *, delete_roles: bool = False
    ) -> int:
        """Supprime tous les salons d'UE de la catégorie.

        Args:
            category: la catégorie dans laquelle supprimer les salons d'UE.
            delete_roles: si True, les rôles associés aux salons sont aussi supprimés

        Returns:
            Le nombre de salons qui ont été supprimés
        """
        ues_names = next(
            (cat.ues for cat in self._bot.settings.categories if cat.id == category.id),
            None,
        )
        if not ues_names:
            return 0
        channels = [c for c in category.text_channels if c.name.upper() in ues_names]
        for channel in channels:
            await self.delete_channel(channel, delete_role=delete_roles)
        return len(channels)

    async def create_category(self, name: str) -> CategoryChannel:
        """Crée une catégorie destinée à contenir des salons d'UEs.

        Args:
            name: le nom de la catégorie à créer.

        Returns:
            La catégorie créée.

        Raises:
            AlreadyExistsError:
                Une catégorie avec le nom donné existe déjà.

            MissingConfigurationError:
                Le nom donné ne correspond à rien dans la configuration.
        """
        guild = self._bot.watched_guild
        settings = self._bot.settings
        name = name.upper()
        if any(c.name == name for c in guild.categories):
            raise AlreadyExistsError
        category_settings = next((c for c in settings.categories if c.name == name), None)
        if category_settings is None:
            raise MissingConfigurationError
        elected_role = guild.get_role(category_settings.elected_role)
        moderator_role = guild.get_role(settings.guild.special_roles.moderator)
        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            moderator_role: PermissionOverwrite(read_messages=True),
            elected_role: PermissionOverwrite(read_message=True),
        }
        return await guild.create_category(
            name, overwrites=overwrites, reason="Création d'une catégorie pour salons d'UEs"
        )

    async def create_channel(self, name: str) -> (TextChannel, Role):
        """Crée un salon d'UE.

        Si ceux-ci n'existent pas encore, crée également :
        - la catégorie à laquelle appartient l'UE
        - le rôle correspondant à l'UE

        Args:
            name: le nom du salon à créer.

        Returns:
            Le salon créé.

        Raises:
            AlreadyExistsError:
                Un salon avec ce nom existe déjà.
            MissingConfigurationError:
                Le nom donné ne correspond à rien dans la configuration.
        """
        guild = self._bot.watched_guild
        settings = self._bot.settings
        name = name.upper()
        if any(c.name == name.lower() for c in guild.text_channels):
            raise AlreadyExistsError

        category_settings = next((c for c in settings.categories if name in c.ues), None)
        if category_settings is None:
            raise MissingConfigurationError
        category = next((c for c in guild.categories if c.id == category_settings.id), None)
        if category is None:
            category = await self.create_category(category_settings.name)

        role = next((r for r in guild.roles if r.name == name), None)
        if role is None:
            role = await guild.create_role(
                name=name, reason=f"Création d'un rôle pour l'UE {name}"
            )

        moderator_role = guild.get_role(self._bot.settings.guild.special_roles.moderator)
        elected = guild.get_role(category_settings.elected_role)
        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            role: PermissionOverwrite(read_messages=True),
            moderator_role: PermissionOverwrite(read_messages=True),
        }
        if elected:
            overwrites[elected] = PermissionOverwrite(read_messages=True)

        return await category.create_text_channel(
            name.lower(), overwrites=overwrites, reason=f"Création d'un salon pour l'UE {name}"
        ), role

    def get_missing_channels(self, category: CategoryChannel = None) -> set[LowerStr]:
        """Renvoie le nom de tous les salons d'UEs manquant sur le serveur."""
        if category:
            ues = {
                LowerStr(ue.lower())
                for ue in next(
                    (cat for cat in self._bot.settings.categories if cat.id == category.id), None
                ).ues
            }
            existing = {
                LowerStr(channel.name)  # les noms des salons Discord sont en minuscule par défaut
                for channel in category.text_channels
            }
            return ues - existing
        ues = {LowerStr(ue.lower()) for cat in self._bot.settings.categories for ue in cat.ues}
        existing = {
            LowerStr(channel.name)  # les noms des salons Discord sont en minuscule par défaut
            for channel in self._bot.watched_guild.text_channels
        }
        return ues - existing
