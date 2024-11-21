from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class JiraIssue:
    summary: str
    status: str
    updated: str
    key: str

    def __post_init__(self):
        self.updated = self.updated.split('T')[0]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            summary=data['fields']['summary'],
            status=data['fields']['status']['name'],
            updated=data['fields']['updated'],
            key=data['key']
        )

    def to_dict(self):
        return {
            'summary': self.summary,
            'status': self.status,
            'updated': self.updated,
            'key': self.key
        }

    def __str__(self):
        return f'Summary: {self.summary}\nStatus: {self.status}\nUpdated at: {self.updated}\nKey: {self.key}\n'


@dataclass
class JiraIssues:
    issues: list[JiraIssue]

    @classmethod
    def from_dict(cls, data: dict):
        issues = [
            JiraIssue.from_dict(issue)
            for issue
            in data['issues']
            if 'fields' in issue
        ]
        return cls(issues)

    def to_dict(self):
        return {
            'issues': [
                issue.to_dict()
                for issue
                in self.issues
                if issue.status != 'Tareas por hacer'
            ]
        }

    def __str__(self):
        return '\n'.join(str(issue) for issue in self.issues)
