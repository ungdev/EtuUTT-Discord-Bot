import ast
from typing import TYPE_CHECKING

import aiohttp_jinja2
from aiohttp import web

from etuutt_bot.services.user import UserService
from etuutt_bot.types import CasUserSchema

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


async def handler(req: web.Request) -> web.Response:
    if req.method != "POST":
        return web.HTTPMethodNotAllowed(req.method, ["POST"])  # HTTP 405
    post = await req.post()
    bot: EtuUTTBot = req.app["bot"]

    if not "etu-info" and "discord-username" in post:
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

    etu_info = CasUserSchema.model_validate(ast.literal_eval(post.get("etu-info")))

    if member := bot.watched_guild.get_member_named(post.get("discord-username")):
        user_service = UserService(bot)
        await user_service.sync(member, etu_info)
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
