from dataclasses import dataclass
from typing import Optional

from .user import GitHubUser
from .repository import GitHubRepository


@dataclass()
class GitHubBaseEvent:
    sender: GitHubUser
    repository: GitHubRepository
    action: Optional[str]
    organization: Optional[dict]
    installation: Optional[dict]
