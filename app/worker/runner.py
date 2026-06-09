import asyncio
import uuid

from app.core.broker import broker
from app.db.session import get_session
from app.db.repositories.task import TaskRepository
from app.shared.enums import TaskStatus
from app.tasks.registry import TASK_REGISTRY

QUEUE_NAME = "default"


async def worker_loop():
    while True:
        print("waiting for task...")

        job = await broker.consume(QUEUE_NAME)

        print("received", job)

        task_id = uuid.UUID(job["task_id"])

        with get_session() as session:
            repo = TaskRepository(session)

            task = repo.get_by_id(task_id)

            if not task:
                print(f"task {task_id} not found")
                continue

            print(f"processing {task.task_name}")

            task.status = TaskStatus.RUNNING
            session.commit()

            try:
                task_func = TASK_REGISTRY[task.task_name]

                result = await task_func(**task.payload)

                task.status = TaskStatus.SUCCESS
                task.result = result

                print("task completed")

            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)

                print("task failed:", e)

            session.commit()


if __name__ == "__main__":
    print("worker booting...")
    print("registered tasks:", TASK_REGISTRY)

    asyncio.run(worker_loop())
