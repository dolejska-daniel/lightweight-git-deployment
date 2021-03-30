from typing import List
from dataclasses import dataclass


@dataclass()
class GitHubCommitAuthor:
    name: str
    email: str


@dataclass()
class GitHubCommit:
    id: str
    timestamp: str
    message: str
    author: GitHubCommitAuthor
    url: str
    distinct: bool
    added: list[str]
    modified: list[str]
    removed: list[str]
