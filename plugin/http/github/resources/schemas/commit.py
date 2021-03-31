from dataclasses import dataclass
from typing import Optional


@dataclass()
class GitHubCommitAuthor:
    name: str
    email: str
    username: Optional[str]


@dataclass()
class GitHubCommit:
    id: str
    tree_id: str
    distinct: bool
    message: str
    timestamp: str
    url: str
    author: GitHubCommitAuthor
    committer: GitHubCommitAuthor
    added: list[str]
    modified: list[str]
    removed: list[str]
