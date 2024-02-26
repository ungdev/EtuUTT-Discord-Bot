from aiohttp import web


async def handler(req: web.Request) -> web.Response:
    # TODO
    return web.Response(text=f"Login successful\n{req.query.get('code')}")
