import asyncio

from app.core.broker import broker
from app.tasks.registry import TASK_REGISTRY

import app.tasks.example  # noqa: F401


QUEUE_NAME = "default"


async def worker_loop():
    print("worker booting...")
    print("registered tasks:", TASK_REGISTRY)

    while True:
        print("waiting for task...")

        job = await broker.consume(QUEUE_NAME)

        print("received", job)

        task_name = job["task"]
        payload = job["payload"]

        task_func = TASK_REGISTRY.get(task_name)

        if not task_func:
            print(f"unknown task {task_name}")
            continue

        try:
            result = await task_func(payload)

            print("task success", result)

        except Exception as e:
            print("task failed", str(e))


if __name__ == "__main__":
    asyncio.run(worker_loop())
