from __future__ import annotations

import logging
from typing import TYPE_CHECKING, assert_never

import discord

from etuutt_bot.types import MemberType

if TYPE_CHECKING:
    from discord import Role

    from etuutt_bot.bot import EtuUTTBot
    from etuutt_bot.routes.role import ApiStudent


class UserService:
    NICKNAME_MAX_LEN = 32

    def __init__(self, bot: EtuUTTBot):
        self._bot = bot

    def get_server_nickname(self, student: ApiStudent) -> str:
        pseudo = f"{student.first_name.title()} {student.last_name.upper()}"
        match student.member_type:
            case MemberType.Student:
                pseudo += " - " + "/".join(map(str, "/".join(student.branch_levels)))
            case MemberType.FormerStudent:
                pseudo += " - Ancien étu"
            case MemberType.Teacher:
                pseudo += " - Enseignant"
            case other:
                assert_never(other)
        if len(pseudo) > self.NICKNAME_MAX_LEN and " " in student.first_name:
            # If he has several first names we only keep the first one
            pseudo = (
                f"{student.first_name.split(' ')[0]} {pseudo.removeprefix(student.first_name)}"
            )
        if len(pseudo) > self.NICKNAME_MAX_LEN:
            # if there is no other way to shorten the nickname, slice it (not ideal)
            logging.warning(f"L'utilisateur {pseudo} est trop long. Vérifiez son pseudo")
            pseudo = pseudo[: self.NICKNAME_MAX_LEN]
        return pseudo

    def get_ue_roles(self, student: ApiStudent) -> set[Role]:
        match student.member_type:
            case MemberType.Student:
                return {
                    discord.utils.find(
                        lambda r, to_find=branch: r.name.upper() == to_find.upper(),
                        self._bot.watched_guild.roles,
                    )
                    for branch in student.branches
                }
            case MemberType.FormerStudent:
                role_id = self._bot.settings.guild.special_roles.former_student
                return {self._bot.watched_guild.get_role(role_id)}
            case MemberType.Teacher:
                role_id = self._bot.settings.guild.special_roles.teacher
                return {self._bot.watched_guild.get_role(role_id)}
            case other:
                assert_never(other)

    async def sync(self, member: discord.Member, data: ApiStudent):
        """Synchronise le membre du serveur avec les données de l'api du site etu.

        Args:
            member: Le membre du serveur Discord à synchroniser
            data: Les données de l'API
        """
        nickname = self.get_server_nickname(data)
        roles = self.get_ue_roles(data)
        if nickname == member.nick and roles <= set(member.roles):
            # user already synced
            return

        upmost_role: Role = max(self._bot.watched_guild.get_member(self._bot.user.id).roles)
        reason_msg = f"Authentification etu de : {member.global_name}"
        if any(r >= upmost_role for r in member.roles):
            # if the bot try to assign a role to a user with a role higher
            # than the bot's highest role, discord returns a 403.
            # Thus, those members must receive their role without using the `edit` method.
            # Moreover, the bot cannot edit their nickname
            roles -= set(member.roles[1:])
            await member.add_roles(*roles, reason=reason_msg)
            return
        roles |= set(member.roles)
        await member.edit(nick=nickname, roles=roles, reason=reason_msg)
