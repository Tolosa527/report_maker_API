from dataclasses import dataclass
from src.clients.parser.github_parser import GitHubIssues
from src.clients.parser.jira_parser import JiraIssues
from src.models.task import Task
from src.logger import Logger


log = Logger().get_logger(__name__)


@dataclass
class OpenAIData:
    github_data: GitHubIssues
    jira_data: JiraIssues
    tasks: list[Task]

    def order_by_date(self) -> dict:
        data: dict = {}
        log.info(f"Processing tasks: {self.tasks}")
        for task in self.tasks:
            if task.date not in data:
                data[task.date] = {
                    'github': [],
                    'jira': [],
                    'tasks': []
                }
            data[task.date]['tasks'].append(task)
        for github_issue in self.github_data.issues:
            if github_issue.updated_at not in data:
                data[github_issue.updated_at] = {
                    'github': [],
                    'jira': [],
                    'tasks': []
                }
            data[github_issue.updated_at]['github'].append(
                github_issue.to_dict()
            )
        for jira_issue in self.jira_data.issues:
            if jira_issue.updated not in data:
                data[jira_issue.updated] = {
                    'github': [],
                    'jira': [],
                    'tasks': []
                }
            data[jira_issue.updated]['jira'].append(
                jira_issue.to_dict()
            )
        return data
