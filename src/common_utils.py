from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orm.models import Drunkard


def get_correct_time_spelling(time: int) -> tuple[str, ...]:
    if time in {11, 12, 13, 14}:
        return 'часов', 'минут', 'секунд'
    if time % 10 == 1:
        return 'час', 'минута', 'секунда'
    if time % 10 in {2, 3, 4}:
        return 'часа', 'минуты', 'секунды'
    return 'часов', 'минут', 'секунд'


def get_correct_count_spelling(count: int) -> str:
    if count in {11, 12, 13, 14}:
        return 'раз'
    if count % 10 == 1:
        return 'раз'
    if count % 10 in {2, 3, 4}:
        return 'раза'
    return 'раз'


def format_time(total_seconds: int) -> str:
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    total_hours = total_minutes // 60

    str_hours = f'{total_hours} {get_correct_time_spelling(total_hours)[0]}' \
        if total_hours else ''
    str_minutes = f'{minutes} {get_correct_time_spelling(minutes)[1]}' \
        if minutes else ''
    str_seconds = f'{seconds} {get_correct_time_spelling(seconds)[2]}' \
        if seconds else ''

    return ' '.join([time_piece for time_piece in [str_hours, str_minutes, str_seconds] if time_piece]).strip()


def map_drunkards_to_id(all_drunkards: Sequence["Drunkard"]) -> dict[int, "Drunkard"]:
    return {drunkard.id: drunkard for drunkard in all_drunkards}
