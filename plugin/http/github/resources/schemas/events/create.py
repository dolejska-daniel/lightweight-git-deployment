from dataclasses import dataclass
from typing import Optional

from .base import GitHubBaseEvent


@dataclass()
class GitHubCreateEvent(GitHubBaseEvent):
    ref: str
    ref_type: str
    master_branch: str
    description: Optional[str]
    pusher_type: str
