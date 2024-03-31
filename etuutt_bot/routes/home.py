from os import getenv

from aiohttp import web


async def handler(req: web.Request) -> web.Response:
    raise web.HTTPFound(  # HTTP 302
        f"{req.app["bot"].settings.etu_api.url}/oauth/authorize"
        f"?client_id={getenv('API_CLIENT_ID')}&response_type=code&state={req.app['api_state']}"
    )
