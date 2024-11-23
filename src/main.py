from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from src.handler import Handler
from src.models.task import TaskResponse
from src.logger import Logger

log = Logger().get_logger(__name__)

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/task", response_model=TaskResponse)
def add_task(message: str) -> TaskResponse:
    handler = Handler(session=Session(engine))
    task = handler.add_task(message=message)
    log.info("Response from add_task: %s", str(task))
    return task


@app.get("/tasks")
def get_tasks(
    start_date: str | None = None,
    end_date: str | None = None
) -> list[TaskResponse] | None:
    handler = Handler(session=Session(engine))
    tasks = handler.get_tasks(start_date=start_date, end_date=end_date)
    log.info("Response from add_task: %s", tasks)
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
    handler = Handler(session=Session(engine))
    report = handler.handle_report(
        start_date=start_date,
        end_date=end_date,
        send_to_slack=True
    )
    return report
