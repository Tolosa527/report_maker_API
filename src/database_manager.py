from sqlmodel import SQLModel, create_engine, select, Session
from src.models.task import Task
from src.logger import Logger
from datetime import datetime

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
log = Logger().get_logger(__name__)


class DatabaseManager:
    def __init__(self):
        self._session = Session(engine)
        SQLModel.metadata.create_all(engine)

    def create_tables(self):
        SQLModel.metadata.create_all(engine)

    def add_task(self, task: Task) -> Task:
        log.info("Adding task: %s", task)
        self._session.add(instance=task)
        try:
            self._session.commit()
            log.info("Task committed successfully")
        except Exception as e:
            log.error("Error committing task: %s", e)
            self._session.rollback()
            raise
        return task

    def get_tasks(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> list[Task]:
        log.info(
            f"Getting tasks from {start_date if start_date else '-'} "
            f"to {end_date if end_date else '-'}"
        )
        query = select(Task)
        if start_date and end_date:
            query = query.where(
                Task.date >= start_date
            ).where(Task.date <= end_date)
        try:
            tasks = self._session.exec(query).all()
            log.info(f"Tasks: {tasks}")
            return tasks
        except Exception as e:
            log.error("Error getting tasks: %s", e)
            raise
