from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord
from discord import Role

from etuutt_bot.config import Settings

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


async def assign_roles(
    bot: EtuUTTBot, guild: discord.Guild, member: discord.Member, etu: dict
) -> None:
    """Assign roles to a member based on a dictionary"""
    roles = set()
    pseudo = f"{etu.get('firstName').title()} {etu.get('lastName').upper()}"
    special_roles = Settings().guild.special_roles
    if etu.get("isStudent"):
        # If formation is empty, it's a former student
        if not etu.get("formation"):
            roles.add(guild.get_role(special_roles.former_student))
            pseudo += " - Ancien étu"
        else:
            roles.add(guild.get_role(special_roles.student))
            ue_roles = {
                discord.utils.find(
                    lambda r, to_find=branch_list: r.name.upper() == to_find.upper(), guild.roles
                )
                for branch_list in etu.get("branch_list")
            }
            if ue_roles:
                roles.update(ue_roles)
            pseudo += " - " + "/".join(map(str, etu.get("branch_level_list")))
    # If member isn't a student, it can only be a teacher
    else:
        roles.add(guild.get_role(special_roles.teacher))

    # TODO: add UEs and create the UE role if not already existant

    # Nickname can only be up to 32 characters long
    if len(pseudo) > 32:
        # If he has several first names we only keep the first one
        if " " in etu.get("firstName"):
            pseudo = (
                f"{etu.get('firstName').split(' ')[0]} {pseudo.split(etu.get('firstName'))[1]}"
            )
        # Else we just slice the pseudo (not ideal)
        else:
            logging.warning(
                f"Le pseudo de l'utilisateur {member.name} est trop long. Vérifiez son pseudo"
            )
            pseudo = pseudo[:32]

    if len(roles) == 0 and pseudo == member.nick:
        # There is nothing to edit
        return

    upmost_role: Role = max(guild.get_member(bot.user.id).roles)
    reason_msg = f"Authentification etu de : {member.global_name}"
    if any(r >= upmost_role for r in member.roles):
        # if the bot try to assign a role to a user with a role higher
        # than the bot's highest role, discord returns a 403.
        # Thus, those members must receive their role without using the `edit` method.
        # Moreover, the bot cannot edit their nickname
        roles -= set(member.roles[1:])
        await member.add_roles(*roles, reason=reason_msg)
        return
    roles.update(set(member.roles))
    await member.edit(nick=pseudo, roles=roles, reason=reason_msg)
