from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from src.handler import Handler
from src.models.task import Task
from typing import Optional

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/message")
def add_task(task: Task):
    handler = Handler(session=Session)
    handler.add_task(task)
    return {"task": task}
    

@app.get("/tasks")
def get_tasks(start_date: Optional[str] = None, end_date: Optional[str] = None):
    handler = Handler(session=Session)
    tasks = handler.get_tasks(start_date=start_date, end_date=end_date)
    return tasks
    
    
@app.get("/reports")
def get_report(start_date: str, end_date: str):
    handler = Handler(session=Session)
    report = handler.handle_report(
        start_date=start_date,
        end_date=end_date,
        send_to_slack=False
    )
    return report
    
@app.get("/send_report")
def send_report(start_date: str, end_date: str):
    handler = Handler(session=Session)
    report = handler.handle_report(
        start_date=start_date,
        end_date=end_date,
        send_to_slack=True
    )
    return report
