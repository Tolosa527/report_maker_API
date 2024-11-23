import os
import json
from dataclasses import dataclass
from typing import Optional, Dict
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class Settings:
    jira_user: str = ""
    jira_api_token: str = ""
    jira_url: str = ""
    github_token: str = ""
    github_username: str = ""
    slack_token: str = ""
    slack_channel_id: str = ""
    github_headers: Optional[Dict[str, str]] = None
    open_ai_api_key: str = ""
    database_name: str = "messages.db"
    debug: bool = False

    def __post_init__(self, **values):
        super().__init__(**values)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_directory, "config.json")
        with open(config_path) as f:
            data = json.load(f)
            self.jira_user = data['jira_user']
            self.jira_api_token = data['jira_api_token']
            self.jira_url = data['jira_url']
            self.github_token = data['github_token']
            self.github_headers = {'Authorization': f'token {self.github_token}'}
            self.slack_token = data['slack_token']
            self.slack_channel_id = data['slack_channel_id']
            self.github_username = data['github_username']
            self.open_ai_api_key = data['open_ai_api_key']
            self.database_name = data.get('database_name', self.database_name)
            self.debug = data.get('debug', self.debug)

    @property
    def get_jira_user(self):
        return self.jira_user

    @property
    def get_jira_api_token(self):
        return self.jira_api_token

    @property
    def get_jira_url(self):
        return self.jira_url

    @property
    def get_github_token(self):
        return self.github_token

    @property
    def get_github_headers(self):
        return self.github_headers

    @property
    def get_slack_token(self):
        return self.slack_token

    @property
    def get_slack_channel_id(self):
        return self.slack_channel_id

    @property
    def get_github_username(self):
        return self.github_username

    @property
    def get_open_ai_api_key(self):
        return self.open_ai_api_key

    @property
    def get_database_name(self):
        return self.database_name

    @property
    def get_debug(self):
        return self.debug

settings = Settings()
