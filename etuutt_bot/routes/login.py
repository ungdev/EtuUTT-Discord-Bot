from aiohttp import web


async def handler(req: web.Request) -> web.Response:
    # TODO
    if not req.query.get("code"):
        return web.Response(status=401)
    return web.Response(text=f"Login successful\n{req.query.get('code')}")
