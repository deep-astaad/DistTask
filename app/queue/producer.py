import asyncio

from app.core.broker import broker
from app.db.models import Task
from app.db.session import get_session


QUEUE_NAME = "default"


async def main():
    with get_session() as session:
        task = Task(
            task_name="debug.sleep",
            payload={
                "seconds": 5,
            },
        )

        session.add(task)

        session.commit()
        session.refresh(task)

        print(f"created task {task.id}")

        await broker.publish(
            QUEUE_NAME,
            {
                "task_id": str(task.id),
            },
        )

        print("published task")


if __name__ == "__main__":
    asyncio.run(main())
