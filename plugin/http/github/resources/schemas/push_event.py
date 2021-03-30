from dataclasses import dataclass
from typing import List

from .base import GitHubBaseEvent
from .commit import GitHubCommit, GitHubCommitAuthor


@dataclass()
class GitHubPushEvent(GitHubBaseEvent):
    ref: str
    before: str
    after: str
    created: bool
    deleted: bool
    base_ref: str
    compare: str
    commits: list[GitHubCommit]
    head_commit: GitHubCommit
    pusher: GitHubCommitAuthor