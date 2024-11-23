from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import BaseModel

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    text: str
    date: datetime


class TaskResponse(BaseModel):
    text: str
    date: datetime

    def __str__(self):
        return f"Task => {self.text} at {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
