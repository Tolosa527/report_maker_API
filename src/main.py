from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session

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
def add_task(task: str):
    ...
    

@app.get("/tasks")
def get_tasks(start_date: str, end_date: str):
    ...
    
    
@app.get("/reports")
def get_report(start_date: str, end_date: str):
    report = self._handle_report(
        start_date=start_date,
        end_date=end_date,
        send_to_slack=False
    )
    return report
    
@app.get("/send_report")
def send_report(start_date: str, end_date: str):
    report = self._handle_report(
        start_date=start_date,
        end_date=end_date,
        send_to_slack=True
    )
    return report
