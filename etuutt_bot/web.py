from __future__ import annotations

import logging
from os import getenv
from typing import TYPE_CHECKING

import aiohttp_jinja2
import jinja2
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

    # Declare app, add error middleware and setup Jinja templates
    app = web.Application(middlewares=[error_middleware])
    aiohttp_jinja2.setup(app, enable_async=True, loader=jinja2.FileSystemLoader("templates"))
    # Declare routes and their associated handler
    app.add_routes(
        [
            web.get("/", home.handler),
            web.get("/login", login.handler),
            web.get("/role", role.handler),
            web.post("/role", role.handler),
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
    try:
        response: web.Response = await handler(req)
        # Check if status code is not in the 400s or 500s
        if not 599 >= response.status >= 400:
            return response

        # Render error template
        response_to_error = await aiohttp_jinja2.render_template_async(
            "http_error.html.jinja",
            req,
            {"status": response.status, "reason": response.reason},
            status=response.status,
        )

        # Add header for 405 Method Not Allowed
        if response_to_error.status == 405:
            response_to_error.headers.add("Allow", response.headers.get("Allow", "GET"))

    # Manage exception
    except web.HTTPError as exception:
        # Render error template
        response_to_error = await aiohttp_jinja2.render_template_async(
            "http_error.html.jinja",
            req,
            {"status": exception.status, "reason": exception.reason},
            status=exception.status,
        )

        # Add header for 405 Method Not Allowed
        if response_to_error.status == 405:
            response_to_error.headers.add("Allow", exception.headers.get("Allow", "GET"))

    return response_to_error
