from os import getenv

import aiohttp_jinja2
from aiohttp import web

from etuutt_bot.utils.assign_roles import assign_roles


async def handler(req: web.Request) -> web.Response:
    if req.method != "POST":
        return web.HTTPMethodNotAllowed(req.method, ["POST"])  # HTTP 405
    post = await req.post()
    if "etu-token" and "discord-username" in post:
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
        async with req.app["bot"].session.get(
            f"{getenv('API_URL')}/public/user/account", params=params
        ) as response:
            if response.status != 200:
                return web.Response(status=response.status)
            resp: dict = (await response.json()).get("data")
            if all(  # Check if the fields we need are present
                field in resp
                for field in [
                    "isStudent",
                    "firstName",
                    "lastName",
                    "formation",
                    "branch_list",
                    "branch_level_list",
                    "uvs",
                ]
            ) and (
                member := req.app["bot"].watched_guild.get_member_named(
                    post.get("discord-username")
                )
            ):
                await assign_roles(req.app["bot"].watched_guild, member, resp)
                return web.Response(text="Roles assigned!")
            # TODO: make better response
            # TODO: handle case where fields not present and discord username is invalid
    return web.HTTPBadRequest()
