import json
from pytest import fixture
from src.clients.parser.github_parser import GitHubIssues
from src.clients.parser.jira_parser import JiraIssues
from src.clients.parser.openai_parser import OpenAIData
from src.clients.parser.tasks_parser import Tasks
from src.db.database import Database
import os


@fixture(scope="session")
def db():
    # Initialize the database once for the entire test session
    database = Database(test_db="tests/test.db")
    database.initialize()
    yield database
    # Teardown the database after the test session
    database.cursor.close()
    os.remove("tests/test.db")


@fixture
def github_data():
    github_data = json.loads(open("tests/github_example.json").read())
    parsed_data = GitHubIssues.from_dicts(github_data, {})
    return parsed_data


@fixture
def jira_data():
    jira_data = json.loads(open("tests/jira_data.json").read())
    parsed_data = JiraIssues.from_dict(jira_data)
    return parsed_data


@fixture
def open_ai_data(github_data, jira_data, db):
    db.add_message("Meeting with Alex and Alfonso SES hopedajes")
    open_ai_parsed_data = OpenAIData(
        github_data=github_data,
        jira_data=jira_data,
        tasks=Tasks.from_list(db.get_messages()),
    )
    return open_ai_parsed_data
