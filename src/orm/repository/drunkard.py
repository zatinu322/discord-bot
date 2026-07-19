from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from orm import get_atomic_session
from orm.models import Drunkard


async def get_all_drunkards() -> Sequence[Drunkard]:
    stmt = select(Drunkard)
    async with get_atomic_session() as session:
        drunkards = await session.scalars(stmt)
        return drunkards.all()


async def get_drunkard_by_id(drunkard_id: int) -> Drunkard | None:
    stmt = select(Drunkard).where(Drunkard.id == drunkard_id)
    async with get_atomic_session() as session:
        drunkard = await session.scalar(stmt)
        return drunkard


async def add_shot_to_drunkard(
    drunkard_id: int,
    drunk_time: int,
    unmute_date: datetime,
    removed_role_ids: list[int] | None,
) -> None:
    stmt = select(Drunkard).where(Drunkard.id == drunkard_id).with_for_update()
    async with get_atomic_session() as session:
        stmt = insert(Drunkard).values(
            id=drunkard_id,
            shots_count=1,
            drunk_time=drunk_time,
            sobriety_date=unmute_date,
            removed_role_ids=removed_role_ids or [],
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[Drunkard.id],
            set_={
                "shots_count": Drunkard.shots_count + 1,
                "drunk_time": Drunkard.drunk_time + stmt.excluded.drunk_time,
                "sobriety_date": stmt.excluded.sobriety_date,
                "removed_role_ids": stmt.excluded.removed_role_ids,
            },
        )

        await session.execute(stmt)
