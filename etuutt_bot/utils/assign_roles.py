import logging

import discord

from etuutt_bot.config import Settings


async def assign_roles(guild: discord.Guild, member: discord.Member, etu: dict) -> None:
    """Assign roles to a member based on a dictionary"""
    roles = set(member.roles)
    pseudo = f"{etu.get('firstName').title()} {etu.get('lastName').upper()}"
    special_roles = Settings().guild.special_roles
    if etu.get("isStudent"):
        # If formation is empty, it's a former student
        if not etu.get("formation"):
            roles.add(guild.get_role(special_roles.former_student_id))
            pseudo += " - Ancien étu"
        else:
            roles.add(guild.get_role(special_roles.student_id))
            roles.update(
                discord.utils.find(
                    lambda r, to_find=branch_list: r.name.upper() == to_find.upper(), guild.roles
                )
                for branch_list in etu.get("branch_list")
            )
            # If no role is found for a branch, it will add None to roles, we then discard it
            roles.discard(None)
            pseudo += " - " + "/".join(map(str, etu.get("branch_level_list")))
    # If member isn't a student, it can only be a teacher
    else:
        roles.add(guild.get_role(special_roles.teacher_id))

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

    await member.edit(nick=pseudo, roles=roles)
