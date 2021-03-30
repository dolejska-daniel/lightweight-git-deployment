from dataclasses import dataclass
from typing import List

from .user import GitHubUser


@dataclass()
class GitHubRelease:
    id: int
    node_id: str
    url: str
    assets_url: str
    upload_url: str
    html_url: str
    tag_name: str
    target_commitish: str
    name: str
    draft: bool
    author: GitHubUser
    prerelease: bool
    created_at: str
    published_at: str
    assets: list[str]
    tarball_url: str
    zipball_url: str
    body: str
