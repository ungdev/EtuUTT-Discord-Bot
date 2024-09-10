from enum import Enum
from typing import NewType

from pydantic import BaseModel, Field

RoleId = NewType("RoleId", int)
ChannelId = NewType("ChannelId", int)

# UpperStr et LowerStr sont des str normaux,
# mais avec l'indication qu'on s'attend à ce qu'ils soient
# entièrement en majuscule ou en minuscule.
UpperStr = NewType("UpperStr", str)
LowerStr = NewType("LowerStr", str)


class MemberType(Enum):
    Student = 1
    FormerStudent = 2
    Teacher = 3


class ApiUserSchema(BaseModel):
    is_student: bool = Field(alias="isStudent")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    formation: str | None
    branches: list[str] | None = Field(alias="branch_list")
    branch_levels: list[str] | None = Field(alias="branch_level_list")
    ues: list[str] = Field(alias="uvs")
    discord_tag: str | None = Field(alias="discordTag")

    @property
    def member_type(self):
        if not self.is_student:
            return MemberType.Teacher
        if not self.formation:
            return MemberType.FormerStudent
        return MemberType.Student
