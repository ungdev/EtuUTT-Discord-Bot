from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfoNotFoundError

import aiohttp
from discord.ext import tasks
from pydantic import ValidationError

from etuutt_bot.services.user import UserService
from etuutt_bot.types import ApiUserSchema

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class SyncService:
    """Service de gestion de la synchronisation des membres du serveur."""

    def __init__(self, bot: EtuUTTBot):
        self._bot = bot

        try:
            from zoneinfo import ZoneInfo

            self._timezone = ZoneInfo(bot.settings.tz)
        # On utilise la timezone UTC en cas de problème
        except ZoneInfoNotFoundError:
            from datetime import timezone

            self._timezone = timezone.utc

        @tasks.loop(time=time(0, tzinfo=self._timezone))
        async def daily_etu_sync():
            self._bot.logger.info("Automatic synchronisation started")
            await self._full_sync()
            self._bot.logger.info("Automatic synchronisation ended")

        if bot.settings.guild.etu_sync:
            daily_etu_sync.start()

        self._daily_etu_sync = daily_etu_sync
        self.is_running = daily_etu_sync.is_running

    async def _full_sync(self):
        api_settings = self._bot.settings.etu_api
        auth = aiohttp.BasicAuth(
            str(api_settings.application_id), api_settings.application_secret.get_secret_value()
        )
        data = {"grant_type": "client_credentials"}
        async with self._bot.session.post(
            f"{api_settings.url}/oauth/token", auth=auth, data=data
        ) as response:
            if response.status != 200:
                self._bot.logger.error(
                    "Failed to get access to API, could not perform automatic synchronisation. "
                    f"{response.status} ; {await response.read()}."
                )
                return
            try:
                token = (await response.json()).get("access_token")
            except KeyError:
                self._bot.logger.error(
                    "Failed to get access to API, could not perform automatic synchronisation. "
                    "No token returned."
                )
                return

        user_service = UserService(self._bot)
        api_url = str(api_settings.url).removesuffix("/api")
        next_page = "/api/public/users"
        params = {"access_token": token, "wantsJoinUTTDiscord": "true"}
        while next_page:
            async with self._bot.session.get(f"{api_url}{next_page}", params=params) as response:
                if response.status != 200:
                    self._bot.logger.error(
                        "Incorrect data, automatic synchronisation stopped midway. "
                        f"{response.status} ; {await response.read()}."
                    )
                resp = await response.json()
            for user in resp.get("data"):
                try:
                    api_user = ApiUserSchema.model_validate(user)
                    if member := self._bot.watched_guild.get_member_named(api_user.discord_tag):
                        await user_service.sync(member, api_user)
                except ValidationError:
                    self._bot.logger.error(f"Incorrect data for {user}")
            next_page = resp.get("pagination").get("next")

    def enable_sync(self):
        self._daily_etu_sync.start()
        self._bot.logger.info("Automatic synchronisation enabled")

    def disable_sync(self):
        self._daily_etu_sync.cancel()
        self._bot.logger.info("Automatic synchronisation disabled")

    async def run_sync(self):
        self._bot.logger.info("Manual synchronisation started")
        await self._full_sync()
        self._bot.logger.info("Manual synchronisation ended")
