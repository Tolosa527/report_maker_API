from src.logger import Logger
from src.clients.parser.github_parser import GitHubIssues
from src.clients.parser.jira_parser import JiraIssues
from src.clients.parser.tasks_parser import Tasks

log = Logger().get_logger(__name__)


def order_by_date(
    tasks: Tasks,
    github_data: GitHubIssues,
    jira_data: JiraIssues
) -> dict:
    data: dict = {}
    log.info(f"Processing tasks: {tasks}")
    for task in tasks.items:
        if task.date not in data:
            data[task.date] = {
                'github': [],
                'jira': [],
                'tasks': []
            }
        data[task.date]['tasks'].append(task)
    for github_issue in github_data.issues:
        if github_issue.updated_at not in data:
            data[github_issue.updated_at] = {
                'github': [],
                'jira': [],
                'tasks': []
            }
        data[github_issue.updated_at]['github'].append(
            github_issue.to_dict()
        )
    for jira_issue in jira_data.issues:
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


# Create a function that recieved a dictionary created by the order_by_date function
# and returns a string with an appropriate format for send the report to slack
# schema of the dictionary:

# {
#     "2021-01-01": {
#         "github": [
#             {
#             "title":"Change return value",
#             "state":"closed",
#             "url":"https://github.com/invibeme/chekin-worker-police-HOS/pull/29",
#             "updated_at":"2024-10-24",
#             "rol":"owner"
#             },
#         ],
#         "jira": [
#            {
#             "summary":"Establishment data registration and validation flow",
#             "status":"Ready for prod",
#             "updated":"2024-10-24",
#             "key":"PLI-1627",
#             "url":"https://jira.atlassian.com/browse/PLI-1627"
#             },
#         ],
#         "tasks": [
#             {
#                 "title": "Create new endpoint",
#                 "date": "2021-01-01",
#             }
#         ]
#     }
# }

def format_report(data: dict) -> str:
    report = ""
    for date, values in data.items():
        report += f"Date: {date}\n"
        report += "Tasks:\n"
        for task in values['tasks']:
            report += f"    - {task['title']}\n"
        report += "GitHub:\n"
        for github in values['github']:
            report += f"    - {github['title']} - {github['state']} - {github['url']} - {github['updated_at']} - {github['rol']}\n"
        report += "Jira:\n"
        for jira in values['jira']:
            report += f"    - {jira['summary']} - {jira['status']} - {jira['updated']} - {jira['key']} - {jira['url']}\n"
        report += "\n"
    return report
