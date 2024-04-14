from typing import TYPE_CHECKING

import aiohttp_jinja2
from aiohttp import web
from pydantic import BaseModel, Field, ValidationError

from etuutt_bot.services.user import UserService
from etuutt_bot.types import MemberType

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class ApiUser(BaseModel):
    is_student: bool = Field(alias="isStudent")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    formation: str | None
    branches: list[str] = Field(alias="branch_list")
    branch_levels: list[str] = Field(alias="branch_level_list")
    ues: list[str] = Field(alias="uvs")

    @property
    def member_type(self):
        if not self.is_student:
            return MemberType.Teacher
        if not self.formation:
            return MemberType.FormerStudent
        return MemberType.Student


async def handler(req: web.Request) -> web.Response:
    if req.method != "POST":
        return web.HTTPMethodNotAllowed(req.method, ["POST"])  # HTTP 405
    post = await req.post()
    bot: EtuUTTBot = req.app["bot"]

    if not "etu-token" and "discord-username" in post:
        return web.HTTPBadRequest()

    if post.get("check-GDPR") != "on":
        return await aiohttp_jinja2.render_template_async(
            "error.html.jinja",
            req,
            {
                "error": "Vous n'avez pas coché la case de consentement RGPD. "
                "Vos données n'ont pas été traitées."
            },
        )

    params = {"access_token": post.get("etu-token")}
    async with bot.session.get(
        f"{bot.settings.etu_api.url}/public/user/account", params=params
    ) as response:
        if response.status != 200:
            return web.Response(status=response.status)
        try:
            resp = (await response.json()).get("data")
            api_student = ApiUser.model_validate(resp)
        except ValidationError:
            return web.HTTPBadRequest()

    if member := bot.watched_guild.get_member_named(post.get("discord-username")):
        user_service = UserService(bot)
        await user_service.sync(member, api_student)
        return web.Response(text="Roles assigned!")
        # TODO: make better response
    return await aiohttp_jinja2.render_template_async(
        "error.html.jinja",
        req,
        {
            "error": "Utilisateur non trouvé dans le serveur. "
            "Avez-vous bien rejoint le serveur Discord ?<br>"
            "Avez-vous bien rentré votre nom d'utilisateur et pas votre nom d'affichage ?"
        },
    )
