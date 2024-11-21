import json
from src.clients.parser.github_parser import GitHubIssues
from src.clients.parser.jira_parser import JiraIssues
from src.clients.parser.tasks_parser import Tasks


def test_github_parser():
    github_data = json.loads(open("tests/github_example.json").read())
    parsed_data = GitHubIssues.from_dicts(github_data, {})

    assert len(parsed_data.issues) == 1
    assert parsed_data.issues[0].title == "[PLI-1198] Add age check for MOS housing in document_issue_date_spain"
    assert parsed_data.issues[0].url == 'https://api.github.com/repos/invibeme/chekin-backend-core/pulls/5548'
    assert parsed_data.issues[0].rol == 'owner'
    assert parsed_data.issues[0].updated_at == '2024-05-28'
    assert parsed_data.issues[0].state == 'open'


def test_jira_parser():
    jira_data = json.loads(open("tests/jira_data.json").read())
    parsed_data = JiraIssues.from_dict(jira_data)

    assert len(parsed_data.issues) == 2
    assert parsed_data.issues[0].key == 'PLI-1295'
    assert parsed_data.issues[0].summary == '[Backend] - Police - Change the timetable for sending data to the police'
    assert parsed_data.issues[0].status == 'Code Review'
    assert parsed_data.issues[0].updated == '2024-09-20'


def test_task_parser(db):
    db.add_message("Meeting with Alex and Alfonso SES hopedajes")
    db.add_message("Meeting with Alex and Alfonso OTA hopedajes")
    messages = db.get_messages()
    assert len(messages) == 2

    tasks = Tasks.from_list(messages)
    item = tasks.items[0]

    assert item.id == 1
    assert item.title == "Meeting with Alex and Alfonso SES hopedajes"
    assert item.date == "2024-09-20"


def test_open_ai_parser(open_ai_data):
    assert open_ai_data
    orginized_data = open_ai_data.order_by_date()
    assert orginized_data
