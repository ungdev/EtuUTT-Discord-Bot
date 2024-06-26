from aiohttp import web

from etuutt_bot.config import ApiConfig


async def handler(req: web.Request) -> web.Response:
    api_settings: ApiConfig = req.app["bot"].settings.etu_api
    raise web.HTTPFound(  # HTTP 302
        f"{api_settings.url}/oauth/authorize"
        f"?client_id={api_settings.client_id}&response_type=code&state={req.app['api_state']}"
    )
