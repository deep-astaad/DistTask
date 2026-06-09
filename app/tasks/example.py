import asyncio

from app.tasks.registry import task


@task("debug.sleep")
async def debug_sleep(seconds: int = 1):
    await asyncio.sleep(seconds)

    return {
        "status": "done",
        "slept": seconds,
    }
