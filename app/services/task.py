from sqlalchemy.orm import Session

from app.db.repositories.task import TaskRepository


class TaskService:
    def __init__(
        self,
        repository: TaskRepository,
    ):
        self.repository = repository

    def acquire_task(
        self,
        session: Session,
        task_id: int,
        worker_id: str,
    ) -> bool:

        return self.repository.mark_running(
            session=session,
            task_id=task_id,
            worker_id=worker_id,
        )

    def mark_success(
        self,
        session: Session,
        task_id: int,
        result_data: dict | None = None,
    ) -> None:

        self.repository.mark_succeeded(
            session=session,
            task_id=task_id,
            result_data=result_data,
        )

    def mark_failure(
        self,
        session: Session,
        task_id: int,
        error_message: str,
    ) -> None:

        self.repository.mark_failed(
            session=session,
            task_id=task_id,
            error_message=error_message,
        )


##TODO: Later implement these
# 1. retry limits
# 2. timeouts
# 3. cancellation checks
# 4. heartbeat validation
# 5. dead letter rules
