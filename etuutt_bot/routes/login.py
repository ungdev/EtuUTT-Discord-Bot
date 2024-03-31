from os import getenv

import aiohttp
import aiohttp_jinja2
from aiohttp import web


async def handler(req: web.Request) -> web.Response:
    # Unauthorized if not code in query string
    if not req.query.get("code") or req.query.get("state") != req.app["api_state"]:
        return web.HTTPUnauthorized()  # HTTP 401
    # Request to obtain the access token
    api_settings = req.app["bot"].settings.etu_api
    auth = aiohttp.BasicAuth(api_settings.client_id, api_settings.client_secret.get_secret_value())
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
    return await aiohttp_jinja2.render_template_async(
        "form.html.jinja",
        req,
        {
            "token": token,
            "discord_link": "https://discord.gg/SH6dutcp",
            "admin": getenv("ADMIN_ID"),
        },
    )
