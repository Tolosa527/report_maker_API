from fastapi import FastAPI
from fastapi.responses import Response

from src.handler import Handler
from src.models.task import TaskResponse
from src.logger import Logger
from src.database_manager import DatabaseManager

log = Logger().get_logger(__name__)

app = FastAPI()
database_manager: DatabaseManager | None = None
handler: Handler | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
def startup_event():
    log.info("Starting up...")
    try:
        global database_manager
        database_manager = DatabaseManager()
        global handler
        handler = Handler(database_manager=database_manager)
    except Exception as e:
        log.error("Error starting up: %s", str(e))
        raise e


@app.post("/task", response_model=TaskResponse)
def add_task(message: str):
    task = handler.add_task(message=message)
    log.info("Response from add_task: %s", str(task))
    return task


@app.get("/tasks")
def get_tasks(
    start_date: str | None = None,
    end_date: str | None = None
) -> list[TaskResponse] | None:
    tasks = handler.get_tasks(start_date=start_date, end_date=end_date)
    log.info("Response from add_task: %s", tasks)
    return tasks


@app.get("/reports")
def get_report(start_date: str, end_date: str):
    report = handler.handle_report(
        start_date=start_date,
        end_date=end_date,
        send_to_slack=False
    )
    return Response(content=report, status_code=200)


@app.get("/send_report")
def send_report(start_date: str, end_date: str):
    report = handler.handle_report(
        start_date=start_date,
        end_date=end_date,
        send_to_slack=True
    )
    return report
