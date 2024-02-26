from __future__ import annotations

import logging
from os import getenv
from typing import TYPE_CHECKING

from aiohttp import web

from etuutt_bot.routes import home, login, role

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


# Web server to authenticate users through the student website to give them roles
async def start_server(client: EtuUTTBot):
    # Set a logger for the webserver
    web_logger = logging.getLogger("web")
    # Don't want to spam logs with site access
    if logging.ERROR > client.log_level >= logging.INFO:
        logging.getLogger("aiohttp.access").setLevel(logging.ERROR)

    app = web.Application(middlewares=[error_middleware])
    app.add_routes(
        [
            web.get("/", home.handler),
            web.get("/login", login.handler),
            web.get("/role", role.handler),
            web.static("/", "public"),
        ]
    )
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, getenv("SERVER_HOST", "0.0.0.0"), int(getenv("SERVER_PORT", 3000)))
    try:
        await site.start()
    except Exception as e:
        web_logger.warning(f"Error while starting the webserver: \n{e}")
    else:
        web_logger.info("The webserver has successfully started")


# Manage errors
@web.middleware
async def error_middleware(req: web.Request, handler) -> web.Response:
    try:  # TODO: add nice error page
        response: web.Response = await handler(req)
        if 500 > response.status >= 400:
            return web.Response(
                text=f"Error {response.status}: {response.reason}", status=response.status
            )
        return response
    except web.HTTPException as e:
        if 500 > e.status >= 400:
            return web.Response(text=f"Error {e.status}: {e.reason}", status=e.status)
        raise