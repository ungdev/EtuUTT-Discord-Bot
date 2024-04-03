from enum import Enum
from typing import Literal

from pydantic import BaseModel, HttpUrl, SecretStr, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from etuutt_bot.types import ChannelId, RoleId


class ActivityType(Enum):
    playing = 0
    streaming = 1
    listening = 2
    watching = 3
    custom = 4
    competing = 5


class BotActivitySettings(BaseModel):
    type: ActivityType
    name: str = ""
    state: str = ""

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, v: str) -> ActivityType:
        try:
            return ActivityType[v]
        except KeyError as e:
            raise ValueError("Not a valid activity type") from e


class BotSettings(BaseModel):
    """Config of the discord client"""

    token: SecretStr
    log_level: Literal["INFO", "DEBUG", "WARNING", "ERROR"] = "INFO"
    status: str = "online"
    activity: BotActivitySettings


class SpecialRolesConfig(BaseModel):
    admin: RoleId
    moderator: RoleId
    student: RoleId
    teacher: RoleId
    former_student: RoleId


class GuildConfig(BaseModel):
    id: int
    channel_admin_id: ChannelId
    special_roles: SpecialRolesConfig
    invite_link: HttpUrl


class CategoryConfig(BaseModel):
    name: str
    id: ChannelId
    elected_role: RoleId
    ues: list[str]


class ApiConfig(BaseModel):
    url: HttpUrl
    client_id: int
    client_secret: SecretStr
    state: str = "xyz"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        toml_file="data/discord.toml",
        env_nested_delimiter="__",
    )

    bot: BotSettings
    guild: GuildConfig
    categories: list[CategoryConfig]
    etu_api: ApiConfig
    server_url: HttpUrl = "http://127.0.0.1:3000"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Define the priority for different sources of configuration.

        The configuration is loaded from the following sources
        (in descending order of priority) :

            1. Arguments passed to the Settings class initialiser.
            2. Environment variables
            3. Variables loaded from the `.env` file.
            4. Variables loaded from the `data/discord.toml` file
            5. The default field values for the Settings model.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
        )
