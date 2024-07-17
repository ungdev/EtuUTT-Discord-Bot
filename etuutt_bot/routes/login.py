import xml.etree.ElementTree as ET

import aiohttp_jinja2
from aiohttp import web

from etuutt_bot.config import AuthConfig, GuildConfig
from etuutt_bot.types import CasUserSchema


async def handler(req: web.Request) -> web.Response:
    # Unauthorized if not code in query string
    api_settings: AuthConfig = req.app["bot"].settings.auth_api
    if not req.query.get("ticket"):
        return web.HTTPUnauthorized()  # HTTP 401
    # Request to obtain the access token
    data = {"service": api_settings.redirect_url, "ticket": req.query.get("ticket")}
    async with req.app["bot"].session.post(
        f"{api_settings.url}/serviceValidate", data=data
    ) as response:
        if response.status != 200:
            return web.Response(status=response.status)
        resp = await response.text()
        try:
            attributes = ET.fromstring(resp)[0][1]
            info = {}
            for attribute in attributes:
                info.update(
                    {attribute.tag.removeprefix("{http://www.yale.edu/tp/cas}"): attribute.text}
                )
            etu_info = CasUserSchema.model_validate(info).model_dump(by_alias=True)
        except IndexError:
            return web.HTTPUnauthorized()  # HTTP 401
        except ET.ParseError:
            return web.HTTPBadRequest()  # HTTP 400
    guild_settings: GuildConfig = req.app["bot"].settings.guild
    return await aiohttp_jinja2.render_template_async(
        "form.html.jinja",
        req,
        {
            "info": etu_info,
            "discord_link": guild_settings.invite_link,
            "admin": guild_settings.special_roles.admin,
        },
    )
