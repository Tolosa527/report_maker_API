from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    date: str
    
    def __repr__(self):
        return f"Task {self.text} {self.date}"
    
    