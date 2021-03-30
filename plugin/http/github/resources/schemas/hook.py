from dataclasses import dataclass
from typing import List


@dataclass()
class GitHubHookConfig:
    content_type: str
    insecure_ssl: str
    secret: str
    url: str


@dataclass()
class GitHubHookResponse:
    code: int
    status: str
    message: str


@dataclass()
class GitHubHook:
    id: int
    type: str
    name: str
    active: bool
    events: list[str]
    config: GitHubHookConfig
    created_at: str
    updated_at: str
    url: str
    test_url: str
    ping_url: str
    last_response: GitHubHookResponse
