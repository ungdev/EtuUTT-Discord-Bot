from os import getenv

import aiohttp
from aiohttp import web


async def handler(req: web.Request) -> web.Response:
    # Unauthorized if not code in query string
    if not req.query.get("code"):
        return web.HTTPUnauthorized()  # HTTP 401
    # Request to obtain the access token
    auth = aiohttp.BasicAuth(getenv("API_CLIENT_ID"), getenv("API_CLIENT_SECRET"))
    async with aiohttp.ClientSession(auth=auth) as session:
        data = {"grant_type": "authorization_code", "code": req.query.get("code")}
        async with session.post(f"{getenv('API_URL')}/oauth/token", data=data) as response:
            if not response.status == 200:
                return web.Response(status=response.status)
            resp = await response.json()
            try:
                token = resp["access_token"]
            except KeyError:
                return web.HTTPBadRequest()  # HTTP 400
    # TODO: display form where user needs to enter discord username
    return web.Response(text=f"Login successful\n{token}")  # Temp return
