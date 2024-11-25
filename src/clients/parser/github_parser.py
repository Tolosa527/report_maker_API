from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from src.clients.parser.filter import FilterType, Status


@dataclass
class GitHubIssue:
    title: str
    state: str
    url: str
    updated_at: str
    rol: str

    def __post_init__(self):
        self.updated_at = self.updated_at.split('T')[0]

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'state': self.state,
            'url': self.url,
            'updated_at': self.updated_at,
            'rol': self.rol
        }


@dataclass
class GitHubIssues:
    issues: List[GitHubIssue] = field(default_factory=list)

    @classmethod
    def from_dicts(
        cls,
        personal_data: dict,
        participation_data: dict
    ) -> GitHubIssues:
        issues = []
        items = personal_data.get('items', [])
        for item in items:
            title = item.get('title', '')
            state = item.get('state', '')
            updated_at = item.get('updated_at', '')
            url = item.get("pull_request", {}).get('url', '')
            issues.append(
                GitHubIssue(
                    title=title,
                    state=state,
                    url=url,
                    updated_at=updated_at,
                    rol='owner'
                )
            )
        items = participation_data.get('items', [])
        for item in items:
            title = item.get('title', '')
            state = item.get('state', '')
            updated_at = item.get('updated_at', '')
            url = item.get("pull_request", {}).get('url', '')
            issues.append(
                GitHubIssue(
                    title=title,
                    state=state,
                    url=url,
                    updated_at=updated_at,
                    rol='participant'
                )
            )
        return cls(issues=issues)

    def to_dict(self) -> dict:
        return {
            'issues': [issue.to_dict() for issue in self.issues]
        }
        
    def filter_by(
        self,
        filter_type: FilterType,
    ):
        pass