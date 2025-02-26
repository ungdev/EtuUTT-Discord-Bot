from __future__ import annotations

import logging
from typing import TYPE_CHECKING, assert_never

import discord

from etuutt_bot.types import MemberType

if TYPE_CHECKING:
    from discord import Role

    from etuutt_bot.bot import EtuUTTBot
    from etuutt_bot.routes.role import ApiUserSchema


class UserService:
    NICKNAME_MAX_LEN = 32

    def __init__(self, bot: EtuUTTBot):
        self._bot = bot

    def get_server_nickname(self, user: ApiUserSchema) -> str:
        """Génère et retourne le pseudo de l'utilisateur affiché sur le serveur Discord."""
        pseudo = f"{user.first_name.title()} {user.last_name.upper()}"
        member_type = user.member_type
        if member_type == MemberType.Student:
            pseudo += " - " + "/".join(user.branch_levels)
        elif member_type == MemberType.FormerStudent:
            pseudo += " - Ancien étu"
        elif member_type == MemberType.Teacher:
            pseudo += " - Enseignant"
        else:
            assert_never(member_type)
        if len(pseudo) > self.NICKNAME_MAX_LEN and " " in user.first_name:
            # If he has several first names we only keep the first one
            pseudo = f"{user.first_name.split(' ')[0]} {pseudo.removeprefix(user.first_name)}"
        if len(pseudo) > self.NICKNAME_MAX_LEN:
            # if there is no other way to shorten the nickname, slice it (not ideal)
            logging.warning(f"Le nom de l'utilisateur {pseudo} est trop long. Vérifiez son pseudo")
            pseudo = pseudo[: self.NICKNAME_MAX_LEN]
        return pseudo

    def get_member_roles(self, user: ApiUserSchema) -> set[Role]:
        """Retourne les rôles qui devraient être attribués à l'utilisateur donné.

        Args:
            user: Les données utilisateur, telles que retournées par l'API du site etu

        Returns:
            L'ensemble des rôles par défaut à donner à l'utilisateur donné.
            C'est-à-dire :
            - Si c'est un étudiant :
                - le rôle `étudiant`
                - le(s) rôle(s) de la ou des branches de sa formation.
                - les rôles correspondant à ses UEs du semestre (s'il en a)
            - Si c'est un ancien étudiant : le rôle `ancien étudiant`
            - Si c'est un enseignant : le rôle `enseignant`
        """
        member_type = user.member_type
        special_ids = self._bot.settings.guild.special_roles
        guild = self._bot.watched_guild
        if member_type == MemberType.Student:
            branches = {r for r in guild.roles if r.name.upper() in user.branches}
            ues = {r for r in guild.roles if r.name.upper() in user.ues}
            return {guild.get_role(special_ids.student)} | branches | ues
        if member_type == MemberType.FormerStudent:
            return {guild.get_role(special_ids.former_student)}
        if member_type == MemberType.Teacher:
            return {guild.get_role(special_ids.teacher)}
        assert_never(member_type)

    async def sync(self, member: discord.Member, user: ApiUserSchema):
        """Synchronise le membre du serveur avec les données de l'api du site etu.

        Args:
            member: Le membre du serveur Discord à synchroniser
            user: Les données de l'API
        """
        nickname = self.get_server_nickname(user)
        roles = self.get_member_roles(user)
        if nickname == member.nick and roles <= set(member.roles):
            # user already synced
            return

        upmost_role: Role = max(self._bot.watched_guild.get_member(self._bot.user.id).roles)
        reason_msg = f"Authentification etu de : {member.global_name}"
        if any(r >= upmost_role for r in member.roles):
            # if the bot try to deal with a role higher
            # than its own highest role, discord returns a 403.
            # Thus, those must be given without using the `edit` method.
            # Moreover, the bot cannot edit the nicknames of users with higher roles.
            roles -= set(member.roles[1:])
            await member.add_roles(*roles, reason=reason_msg)
            return
        roles |= set(member.roles)
        await member.edit(nick=nickname, roles=roles, reason=reason_msg)
