import asyncio

from app.tasks.registry import task


@task("debug.sleep")
async def debug_sleep(payload):
    seconds = payload.get("seconds", 1)

    await asyncio.sleep(seconds)

    return {
        "status": "done",
        "slept": seconds,
    }
