from __future__ import annotations

import logging
from os import getenv
from pathlib import Path
from typing import TYPE_CHECKING

from aiohttp import web

if TYPE_CHECKING:
    from bot import EtuUTTBot


# Add a basic HTTP server to check if the bot is up
async def start_server(client: EtuUTTBot):
    # Set a logger for the webserver
    web_logger = logging.getLogger("web")
    # Don't want to spam logs with site access
    if logging.ERROR > client.log_level >= logging.INFO:
        logging.getLogger("aiohttp.access").setLevel(logging.ERROR)

    app = web.Application()
    app.add_routes(
        [
            web.get("/", handler),
            web.get("/favicon.ico", favicon),
            web.get("/stylesheets/{stylesheet}", stylesheets),
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


# This is the general handler
async def handler(req: web.Request):
    return web.Response(
        body=Path("public_html", "connexion.html").read_text(),
        content_type="text/html",
    )


# This is the favicon handler
async def favicon(req: web.Request):
    return web.Response(
        body=Path("public_html", "favicon.ico").read_bytes(),
        content_type="image/x-icon",
    )


# This is the stylesheets handler
async def stylesheets(req: web.Request):
    if Path("public_html", "stylesheets", req.match_info["stylesheet"]).exists():
        return web.Response(
            body=Path("public_html", "stylesheets", req.match_info["stylesheet"]).read_text(),
            content_type="stylesheet/css",
        )
    return web.Response(status=404)
