from dataclasses import dataclass
from src.logger import Logger

log = Logger().get_logger(__name__)


@dataclass
class Task:
    title: str
    date: str

    def __post_init__(self):
        self.date = self.date.split(' ')[0]

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'date': self.date
        }


@dataclass
class Tasks:
    items: list[Task]

    @classmethod
    def from_list(cls, tasks: list[tuple]) -> 'Tasks':
        log.info(f"Tasks: {tasks}")
        try:
            return cls(
                items=[
                    Task(
                        title=task[1],
                        date=task[2]
                    )
                    for task in tasks
                ]
            )
        except Exception as e:
            log.error(f"Error parsing tasks: {e}")
            raise e

    def to_dict(self) -> list[dict]:
        return [task.to_dict() for task in self.items]
