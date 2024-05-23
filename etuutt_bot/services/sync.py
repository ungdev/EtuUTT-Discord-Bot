from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfoNotFoundError

import aiohttp
from discord.ext import tasks
from pydantic import BaseModel, Field, ValidationError

from etuutt_bot.services.user import UserService
from etuutt_bot.types import MemberType

if TYPE_CHECKING:
    from etuutt_bot.bot import EtuUTTBot


class ApiUserSchema(BaseModel):
    is_student: bool = Field(alias="isStudent")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    formation: str | None
    branches: list[str] = Field(alias="branch_list")
    branch_levels: list[str] = Field(alias="branch_level_list")
    ues: list[str] = Field(alias="uvs")
    discord_tag = Field(alias="discordTag")

    @property
    def member_type(self):
        if not self.is_student:
            return MemberType.Teacher
        if not self.formation:
            return MemberType.FormerStudent
        return MemberType.Student


async def sync(bot: EtuUTTBot):
    # Get local timezone
    try:
        from zoneinfo import ZoneInfo

        my_timezone = ZoneInfo(bot.settings.bot.tz)
    # Use timezone UTC as a fallback
    except ZoneInfoNotFoundError:
        from datetime import timezone

        my_timezone = timezone.utc

    @tasks.loop(time=time(0, tzinfo=my_timezone))
    async def daily_etu_sync():
        api_settings = bot.settings.etu_api
        auth = aiohttp.BasicAuth(
            str(api_settings.client_id), api_settings.client_secret.get_secret_value()
        )
        data = {"grant_type": "client_credentials"}
        async with bot.session.post(
            f"{api_settings.url}/oauth/token", auth=auth, data=data
        ) as response:
            if response.status != 200:
                bot.logger.error(
                    "Failed to get access to API, could not perform automatic synchronisation"
                )
                return
            try:
                token = (await response.json()).get("access_token")
            except KeyError:
                bot.logger.error(
                    "Failed to get access to API, could not perform automatic synchronisation"
                )
                return

        user_service = UserService(bot)
        api_url = api_settings.url.replace("/api", "")
        next_page = "/api/public/users"
        params = {"access_token": token, "wantsJoinUTTDiscord": True}
        while next_page:
            async with bot.session.get(f"{api_url}{next_page}", params=params) as response:
                if response.status != 200:
                    bot.logger.error("Incorrect data, automatic synchronisation stopped midway")
                resp = await response.json()
            for user in resp.get("data"):
                try:
                    api_user = ApiUserSchema.model_validate(user)
                    member = bot.watched_guild.get_member(api_user.discord_tag)
                    await user_service.sync(member, api_user)
                except ValidationError:
                    bot.logger.error("Incorrect data, automatic synchronisation stopped midway")
            next_page = resp.get("pagination").get("next")

    if bot.settings.guild.etu_sync:
        daily_etu_sync.start()
    # TODO: commands to enable/disable auto sync
