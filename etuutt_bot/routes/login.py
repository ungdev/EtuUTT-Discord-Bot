import aiohttp
import aiohttp_jinja2
from aiohttp import web

from etuutt_bot.config import ApiConfig, GuildConfig


async def handler(req: web.Request) -> web.Response:
    # Unauthorized if not code in query string
    api_settings: ApiConfig = req.app["bot"].settings.etu_api
    if not req.query.get("code") or req.query.get("state") != api_settings.state:
        return web.HTTPUnauthorized()  # HTTP 401
    # Request to obtain the access token
    auth = aiohttp.BasicAuth(
        str(api_settings.client_id), api_settings.client_secret.get_secret_value()
    )
    data = {"grant_type": "authorization_code", "code": req.query.get("code")}
    async with req.app["bot"].session.post(
        f"{api_settings.url}/oauth/token", auth=auth, data=data
    ) as response:
        if response.status != 200:
            return web.Response(status=response.status)
        resp = await response.json()
        try:
            token = resp["access_token"]
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
