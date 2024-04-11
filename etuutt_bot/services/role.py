from __future__ import annotations

import itertools
import operator
from enum import Enum
from functools import reduce
from typing import TYPE_CHECKING, assert_never

from discord import Permissions, Role

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class MergeStrategy(Enum):
    """Stratégie pour la fusion de plusieurs objets."""

    Intersection = 1
    """On garde l'intersection. ex: `[a, b, c] & [b, c, d] => [b, c,]`."""
    Union = 2
    """On garde l'union. ex: `[a, b, c] | [b, c, d] => [a, b, c, d]`."""
    Clear = 3
    """On ne garde rien. ex: `[a, b, c] | [b, c, d] => []`"""


class RoleService:
    """Service de gestion des rôles du serveur."""

    def __init__(self, bot: EtuUTTBot):
        self._bot = bot

    def get_duplicates(self, *, case_sensitive: bool = True) -> list[list[Role]]:
        """Cherche et retourne tous les rôles qui sont dupliqués.

        Returns:
            La liste des listes de duplication.
            Chaque élément de la liste est une liste dont tous les
            éléments sont des rôles dupliqués.
        """

        def sort_key(r):
            return r.name if case_sensitive else r.name.lower()

        roles = iter(sorted(self._bot.watched_guild.roles, key=sort_key))

        res = []
        for _, group in itertools.groupby(roles):
            group = list(group)
            if len(group) > 1:
                res.append(group)
        return res

    def get_duplicate(self, role: Role, *, case_sensitive: bool = True) -> list[Role]:
        """Cherche et retourne tous les rôles qui ont le même nom que le rôle donné.

        Returns:
            La liste des rôles dupliqués.
            Le rôle passé en paramètre est inclus dedans.
        """
        if case_sensitive:
            return [r for r in self._bot.watched_guild.roles if r.name == role.name]
        return [r for r in self._bot.watched_guild.roles if r.name.lower() == role.name.lower()]

    @staticmethod
    def combined_perms(roles: list[Role], *, merge_strategy: MergeStrategy) -> Permissions:
        """Calcule et renvoie le jeu de permissions correspondant à la stratégie donnée.
        Args:
            roles: les rôles dont on veut combiner les permissions
            merge_strategy: la stratégie de combinaison des permissions

        Returns:
            Le jeu de permission obtenu par la combinaison des permissions de tous les rôles
        """
        perms = [role.permissions for role in roles]
        if merge_strategy == MergeStrategy.Intersection:
            return reduce(operator.or_, perms)
        if merge_strategy == MergeStrategy.Union:
            return reduce(operator.and_, perms)
        if merge_strategy == MergeStrategy.Clear:
            return Permissions.none()
        assert_never(merge_strategy)

    async def merge(self, roles: list[Role], *, merge_perms_strategy: MergeStrategy):
        to_keep = roles[0]
        # membres à qui il faut donner le rôle qu'on garde
        members = {
            member for role in roles for member in role.members if to_keep not in member.roles
        }
        for member in members:
            await member.add_roles(to_keep)
        await to_keep.edit(
            permissions=self.combined_perms(roles, merge_strategy=merge_perms_strategy)
        )