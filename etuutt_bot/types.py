from enum import Enum
from typing import NewType

RoleId = NewType("RoleId", int)
ChannelId = NewType("ChannelId", int)


class MemberType(Enum):
    Student = 1
    FormerStudent = 2
    Teacher = 3
