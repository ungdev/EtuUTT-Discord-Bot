from enum import Enum
from typing import Literal

from pydantic import BaseModel, HttpUrl, SecretStr, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


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
    admin: int
    moderator: int
    student: int
    teacher: int
    former_student: int


class GuildConfig(BaseModel):
    id: int
    channel_admin_id: int
    special_roles: SpecialRolesConfig


class CategoryConfig(BaseModel):
    name: str
    id: int
    elected_role: int
    ues: list[str]


class ApiConfig(BaseModel):
    url: HttpUrl
    client_id: int
    client_secret: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file="data/discord.toml", extra=None)

    bot: BotSettings
    guild: GuildConfig
    categories: list[CategoryConfig]
    etu_api: ApiConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
