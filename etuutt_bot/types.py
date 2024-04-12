from enum import Enum
from typing import NewType

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
