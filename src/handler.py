# import json
# from src.clients.github_client import (
#     get_github_data,
#     get_paticipation_data
# )
# from src.clients.open_ai import generate_report_text
# from src.clients.jira_client import get_jira_data
# from src.clients.slack_client import send_slack_message
# from src.clients.parser.openai_parser import OpenAIData
# from src.clients.parser.jira_parser import JiraIssues
# from src.clients.parser.github_parser import GitHubIssues
from src.models.task import Task
from src.settings import settings
from sqlmodel import Session, select
from src.logger import Logger

log = Logger().get_logger(__name__)


class Handler:

    def __init__(self, session: Session) -> None:
        self._session = session

    # def handle_report(
    #     self,
    #     start_date: str,
    #     end_date: str,
    #     session: Session,
    #     send_to_slack: bool = False,
    # ) -> str | None:
    #     db_tasks = Tasks.from_list(
    #         self.db.get_messages(
    #             start_date=start_date,
    #             end_date=end_date
    #         )
    #     )
    #     personal_github_data = get_github_data(
    #         username=settings.get_github_username,
    #         start_date=start_date,
    #         end_date=end_date
    #     )
    #     participation_data = get_paticipation_data(
    #         username=settings.get_github_username,
    #         start_date=start_date,
    #         end_date=end_date
    #     )
    #     jira_data = get_jira_data(
    #         username=settings.get_jira_user,
    #         start_date=start_date,
    #         end_date=end_date
    #     )
    #     jira_issues = JiraIssues.from_dict(jira_data)
    #     github_issues = GitHubIssues.from_dicts(
    #         personal_data=personal_github_data,
    #         participation_data=participation_data
    #     )
    #     string_data = json.dumps({
    #             "tasks": db_tasks.to_dict(),
    #             "github_data": github_issues.to_dict(),
    #             "jira_data": jira_issues.to_dict()
    #         })
    #     if send_to_slack:
    #         data = OpenAIData(
    #             github_data=github_issues,
    #             jira_data=jira_issues,
    #             tasks=db_tasks
    #         )
    #         ordered_data = data.order_by_date()
    #         log.info(f"Ordered data: {ordered_data}")
    #         text = generate_report_text(data=ordered_data)
    #         return text
    #     else:
    #         return f"Report generated: {start_date} - {end_date}: {string_data}"
        ...

    def add_task(self, message: str) -> Task:
        task = Task(message=message)
        return task
        
    def get_tasks(self, start_date: str, end_date: str) -> list[str]:
        tasks = self._session.execute(select(Task))
        return tasks
