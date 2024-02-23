from aiohttp import web


async def handler(req: web.Request) -> web.Response:
    # TODO
    return web.Response(text="Login")
