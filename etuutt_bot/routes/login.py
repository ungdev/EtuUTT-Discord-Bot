import aiohttp_jinja2
from aiohttp import web

from etuutt_bot.config import ApiConfig, GuildConfig


async def handler(req: web.Request) -> web.Response:
    # Unauthorized if not code in query string
    api_settings: ApiConfig = req.app["bot"].settings.etu_api
    if not (token := req.query.get("token")):
        return web.HTTPUnauthorized()  # HTTP 401

    # Check if token is valid
    headers = {"Authorization": f"Bearer {token}"}
    async with req.app["bot"].session.get(
        f"{api_settings.url}/auth/signin", headers=headers
    ) as response:
        if response.status != 200:
            return web.Response(status=response.status)
        resp = await response.json()
        try:
            is_valid = resp["valid"]
            if not is_valid:
                return web.HTTPBadRequest()
        except KeyError:
            return web.HTTPBadRequest()  # HTTP 400

    guild_settings: GuildConfig = req.app["bot"].settings.guild
    return await aiohttp_jinja2.render_template_async(
        "form.html.jinja",
        req,
        {
            "token": token,
            "discord_link": guild_settings.invite_link,
            "admin": guild_settings.special_roles.admin,
        },
    )
