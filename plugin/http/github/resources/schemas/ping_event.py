from dataclasses import dataclass

from .base import GitHubBaseEvent
from .hook import GitHubHook


@dataclass()
class GitHubPingEvent(GitHubBaseEvent):
    zen: str
    hook_id: int
    hook: GitHubHook
