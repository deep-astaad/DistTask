from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.models import Task
from app.shared.enums import TaskStatus


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(
        self,
        task_id: UUID,
    ) -> Task | None:
        stmt = select(Task).where(Task.id == task_id)

        return self.session.scalar(stmt)

    def mark_running(
        self,
        task_id: UUID,
        worker_id: str,
    ) -> bool:
        result = self.session.execute(
            update(Task)
            .where(
                Task.id == task_id,
                Task.status == TaskStatus.PENDING,
            )
            .values(
                status=TaskStatus.RUNNING,
                worker_id=worker_id,
                started_at=datetime.now(timezone.utc),
            )
        )

        return result.rowcount == 1

    def mark_succeeded(
        self,
        task_id: UUID,
        result_data: dict | None = None,
    ) -> None:
        self.session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(
                status=TaskStatus.SUCCESS,
                completed_at=datetime.now(timezone.utc),
                result=result_data,
            )
        )

    def mark_failed(
        self,
        task_id: UUID,
        error_message: str,
    ) -> None:
        self.session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(
                status=TaskStatus.FAILED,
                completed_at=datetime.now(timezone.utc),
                error=error_message,
            )
        )

    def save(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
