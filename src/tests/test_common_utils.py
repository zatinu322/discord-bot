from collections.abc import Sequence
from dataclasses import dataclass

import pytest

from common_utils import format_time, get_correct_count_spelling, get_correct_time_spelling, map_drunkards_to_id


@dataclass
class DrunkardMock:
    id: int


DRUNKARDS = [
    DrunkardMock(id=1),
    DrunkardMock(id=555),
]


@pytest.mark.parametrize(
    'time, expected_output', (
        (11, ('часов', 'минут', 'секунд')),
        (12, ('часов', 'минут', 'секунд')),
        (13, ('часов', 'минут', 'секунд')),
        (14, ('часов', 'минут', 'секунд')),
        (1, ('час', 'минута', 'секунда')),
        (21, ('час', 'минута', 'секунда')),
        (101, ('час', 'минута', 'секунда')),
        (2, ('часа', 'минуты', 'секунды')),
        (3, ('часа', 'минуты', 'секунды')),
        (4, ('часа', 'минуты', 'секунды')),
        (22, ('часа', 'минуты', 'секунды')),
        (23, ('часа', 'минуты', 'секунды')),
        (24, ('часа', 'минуты', 'секунды')),
        (102, ('часа', 'минуты', 'секунды')),
        (103, ('часа', 'минуты', 'секунды')),
        (104, ('часа', 'минуты', 'секунды')),
        (5, ('часов', 'минут', 'секунд')),
        (15, ('часов', 'минут', 'секунд')),
        (25, ('часов', 'минут', 'секунд')),
        (105, ('часов', 'минут', 'секунд')),
    ),
)
def test_get_correct_time_spelling(time: int, expected_output: tuple[str, ...]) -> None:
    assert get_correct_time_spelling(time) == expected_output


@pytest.mark.parametrize('count, expected_output', (
    (11, 'раз'),
    (12, 'раз'),
    (13, 'раз'),
    (14, 'раз'),
    (1, 'раз'),
    (21, 'раз'),
    (101, 'раз'),
    (2, 'раза'),
    (3, 'раза'),
    (4, 'раза'),
    (22, 'раза'),
    (23, 'раза'),
    (24, 'раза'),
    (102, 'раза'),
    (103, 'раза'),
    (104, 'раза'),
    (5, 'раз'),
    (15, 'раз'),
    (25, 'раз'),
    (105, 'раз'),
))
def test_get_correct_count_spelling(count: int, expected_output: str) -> None:
    assert get_correct_count_spelling(count) == expected_output


@pytest.mark.parametrize('total_seconds, expected_output', (
    (5, '5 секунд'),
    (65, '1 минута 5 секунд'),
    (3605, '1 час 5 секунд'),
    (3665, '1 час 1 минута 5 секунд'),
    (10605, '2 часа 56 минут 45 секунд'),
))
def test_format_time(total_seconds: int, expected_output: str) -> None:
    assert format_time(total_seconds) == expected_output


@pytest.mark.parametrize(
    'drunkards, expected_output',
    (
        (DRUNKARDS, {1: DRUNKARDS[0], 555: DRUNKARDS[1]}),
        ([], {}),
    ),
)
def test_map_drunkards_to_id(drunkards: Sequence[DrunkardMock], expected_output: dict[int, DrunkardMock]) -> None:
    assert map_drunkards_to_id(drunkards) == expected_output  # type: ignore
