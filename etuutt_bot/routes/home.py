from os import getenv

from aiohttp import web


async def handler(req: web.Request) -> web.Response:
    raise web.HTTPFound(
        f"{getenv('API_URL')}/oauth/authorize"
        f"?client_id={getenv('API_CLIENT_ID')}&response_type=code&state={getenv('API_STATE')}"
    )
