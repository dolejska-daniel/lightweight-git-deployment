from dataclasses import dataclass

from .base import GitHubBaseEvent
from .release import GitHubRelease


@dataclass()
class GitHubReleaseEvent(GitHubBaseEvent):
    release: GitHubRelease
