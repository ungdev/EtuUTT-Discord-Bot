from __future__ import annotations

import logging
import secrets
from typing import TYPE_CHECKING

import aiohttp_jinja2
import jinja2
from aiohttp import web

from etuutt_bot.routes import home, login, role

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


async def start_server(bot: EtuUTTBot) -> web.AppRunner:
    """Start the web server to authenticate users through the student website."""
    # Set a logger for the webserver
    web_logger = logging.getLogger("web")
    # Don't want to spam logs with site access
    if logging.ERROR > bot.log_level >= logging.INFO:
        logging.getLogger("aiohttp.access").setLevel(logging.ERROR)

    # Declare app, add error middleware and setup Jinja templates
    app = web.Application(middlewares=[error_middleware])
    aiohttp_jinja2.setup(app, enable_async=True, loader=jinja2.FileSystemLoader("templates"))
    # Add bot to app
    app["bot"] = bot
    # Generate API state on start
    app["api_state"] = secrets.token_hex()
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
    site = web.TCPSite(runner, bot.settings.server_url.host, bot.settings.server_url.port)
    try:
        await site.start()
    except Exception as e:
        web_logger.warning(f"Error while starting the webserver: \n{e}")
    else:
        web_logger.info("The webserver has successfully started")
    return runner


async def error_handler(req: web.Request, orig_resp: web.Response) -> web.Response:
    """Return a response according to the HTTP status code."""
    # Render error template
    template = await aiohttp_jinja2.render_template_async(
        "http_error.html.jinja",
        req,
        {"status": orig_resp.status, "reason": orig_resp.reason},
        status=orig_resp.status,
    )

    # Add header for 405 Method Not Allowed
    if template.status == 405:
        template.headers.add("Allow", orig_resp.headers.get("Allow", "GET"))

    return template


@web.middleware
async def error_middleware(req: web.Request, handler) -> web.Response:
    """Middleware that handles HTTP Errors (400s and 500s)."""
    try:
        response: web.Response = await handler(req)
        # Check if status code is not in the 400s or 500s
        if not 599 >= response.status >= 400:
            return response

        response_to_error = error_handler(req, response)

    # In case we got an exception while processing a request
    except web.HTTPError as exception:
        response_to_error = error_handler(req, exception)

    return await response_to_error
