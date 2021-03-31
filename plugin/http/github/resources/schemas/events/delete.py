from dataclasses import dataclass

from .base import GitHubBaseEvent


@dataclass()
class GitHubDeleteEvent(GitHubBaseEvent):
    ref: str
    ref_type: str
    pusher_type: str
