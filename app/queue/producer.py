import asyncio

from app.core.broker import broker


async def main():
    await broker.publish(
        "default",
        {
            "task": "debug.sleep",
            "payload": {
                "seconds": 5,
            },
        },
    )

    print("task published")


asyncio.run(main())
