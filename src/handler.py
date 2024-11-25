import json
from src.clients.github_client import (
    get_github_data,
    get_paticipation_data
)
from src.clients.open_ai import generate_report_text
from src.clients.jira_client import get_jira_data
from src.clients.slack_client import send_slack_message
from src.clients.parser.openai_parser import OpenAIData
from src.clients.parser.jira_parser import JiraIssues
from src.clients.parser.github_parser import GitHubIssues
from src.models.task import Task, TaskResponse
from src.settings import settings
from src.logger import Logger
from datetime import datetime
from src.database_manager import DatabaseManager

log = Logger().get_logger(__name__)


class Handler:

    def __init__(self, database_manager: DatabaseManager) -> None:
        self.database_manager = database_manager

    def __get_datetime(
        self,
        start_date: str,
        end_date: str
    ) -> tuple[datetime, datetime]:
        start_dt = datetime.strptime(
            start_date + " 00:00:00", "%Y-%m-%d %H:%M:%S"
        )
        end_dt = datetime.strptime(
            end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S"
        )
        return start_dt, end_dt

    def handle_report(
        self,
        start_date: str,
        end_date: str,
        send_to_slack: bool = False,
    ) -> str | None:
        if not start_date or not end_date:
            return "Please provide start and end dates"
        start_dt, end_dt = self.__get_datetime(start_date, end_date)
        db_tasks = self.database_manager.get_tasks(
            start_date=start_dt, end_date=end_dt
        )
        jira_data = get_jira_data(
            username=settings.get_jira_user,
            start_date=start_dt,
            end_date=end_dt
        )
        jira_issues = JiraIssues.from_dict(jira_data)
        personal_github_data = get_github_data(
            username=settings.get_github_username,
            start_date=start_dt,
            end_date=end_dt
        )
        participation_data = get_paticipation_data(
            username=settings.get_github_username,
            start_date=start_dt,
            end_date=end_dt,
        )
        github_issues = GitHubIssues.from_dicts(
            personal_data=personal_github_data,
            participation_data=participation_data
        )
        string_data = json.dumps({
                "tasks": db_tasks,
                "github_data": github_issues.to_dict(),
                "jira_data": jira_issues.to_dict()
            })
        if send_to_slack:
            data = OpenAIData(
                github_data=github_issues,
                jira_data=jira_issues,
                tasks=db_tasks
            )
            ordered_data = data.order_by_date()
            log.info(f"Ordered data: {ordered_data}")
            text = generate_report_text(data=ordered_data)
            if text:
                log.info(f"Sending slack message: {text}")
                send_slack_message(text=text)
                return "Report sent to slack successfully"
            else:
                return "Error sending slack message"
        else:
            return f"Report generated: {start_date} - {end_date}: {string_data}"

    def add_task(self, message: str) -> Task:
        current_datetime = datetime.now()
        task = Task(text=message, date=current_datetime)
        return self.database_manager.add_task(task=task)

    def get_tasks(
        self,
        start_date: str | None = None,
        end_date: str | None = None
    ) -> list[TaskResponse] | None:
        if start_date and end_date:
            start_dt, end_dt = self.__get_datetime(start_date, end_date)
        tasks = self.database_manager.get_tasks(
            start_date=start_dt if start_date else None,
            end_date=end_dt if end_date else None
        )
        return [TaskResponse(text=task.text, date=task.date) for task in tasks]
