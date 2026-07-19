from dataclasses import dataclass
from datetime import datetime

import pytest

from bot.helpers import ScheduledDrunkard, get_drunk_members


@dataclass
class MemberMock:
    def __init__(self, member_id: int, member_roles: list[str]) -> None:
        self.id = member_id
        self.roles = member_roles


@dataclass
class DrunkardMock:
    sobriety_date: datetime | None


MEMBERS = [
    MemberMock(555, ['muted', 'trusted']),
    MemberMock(666, ['trusted']),
    MemberMock(777, ['muted']),
    MemberMock(888, ['muted']),
    MemberMock(999, ['muted']),
]

DRUNKARDS = {
    555: DrunkardMock(sobriety_date=datetime(2025, 7, 19, 22, 51, 19)),
    666: DrunkardMock(sobriety_date=datetime(2025, 7, 19, 22, 51, 19)),
    777: DrunkardMock(sobriety_date=None),
}

DRUNK_MEMBERS_UNMUTE = [
    ScheduledDrunkard(member=MEMBERS[0], seconds_left=0),
    ScheduledDrunkard(member=MEMBERS[2], seconds_left=0),
]

DRUNK_MEMBERS_SCHEDULE = [
    ScheduledDrunkard(member=MEMBERS[0], seconds_left=38590.0),
    ScheduledDrunkard(member=MEMBERS[2], seconds_left=0),
]


@pytest.mark.parametrize('current_datetime, expected_output', (
    (datetime(2025, 7, 19, 23, 8, 8), DRUNK_MEMBERS_UNMUTE),
    (datetime(2025, 7, 19, 12, 8, 9), DRUNK_MEMBERS_SCHEDULE),
))
def test_get_drunk_members(
    current_datetime: datetime,
    expected_output: list[dict],
) -> None:
    drunk_members = get_drunk_members(
        (member for member in MEMBERS),
        'muted',
        DRUNKARDS,  # type: ignore
        current_datetime,
    )
    assert drunk_members == expected_output
