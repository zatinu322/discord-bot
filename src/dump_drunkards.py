import asyncio
import json

from orm.repository.drunkard import get_all_drunkards


async def main() -> None:
    drunkards = await get_all_drunkards()
    drunkards_for_dump = {
        drunkard.id: {
            "shots_count": drunkard.shots_count,
            "drunk_time": drunkard.drunk_time,
            "sobriety_date": drunkard.sobriety_date.strftime("%Y-%m-%d %H:%M:%S"),
        } for drunkard in drunkards
    }

    print(json.dumps(drunkards_for_dump, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
