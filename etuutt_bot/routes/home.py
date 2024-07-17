from aiohttp import web

from etuutt_bot.config import AuthConfig


async def handler(req: web.Request) -> web.Response:
    api_settings: AuthConfig = req.app["bot"].settings.auth_api
    return web.HTTPFound(  # HTTP 302
        f"{api_settings.url}/login?service={api_settings.redirect_url}"
    )
