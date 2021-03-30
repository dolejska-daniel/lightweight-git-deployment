from pathlib import Path
from typing import Any

from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPAccepted, HTTPBadRequest

from deployer.config import AppConfig
from deployer.utils import dataclass_from_dict, dataclass_select_class_by_dict, get_key_recursive
from deployer.utils.schemas import EventBinding

from .routes import routes
from .schemas.ping_event import GitHubPingEvent
from .schemas.push_event import GitHubPushEvent
from .schemas.release_event import GitHubReleaseEvent

event_classes = [
    GitHubPingEvent,
    GitHubPushEvent,
    GitHubReleaseEvent,
]


@routes.get("/github")
async def github_webhook_handler(request: Request):
    if request.headers.get("Content-Type", "") == "application/json":
        data = dict(await request.json())

    else:
        data = dict(await request.post())

    data = {
            "zen": "Speak like a human.",
            "hook_id": 289352069,
            "hook": {
                "type": "Repository",
                "id": 289352069,
                "name": "web",
                "active": True,
                "events": [
                    "*"
                ],
                "config": {
                    "content_type": "json",
                    "insecure_ssl": "0",
                    "secret": "********",
                    "url": "http://kaidou-ren.srv.dolejska.me:8085/github"
                },
                "updated_at": "2021-03-30T14:52:11Z",
                "created_at": "2021-03-30T14:52:11Z",
                "url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/hooks/289352069",
                "test_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/hooks/289352069/test",
                "ping_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/hooks/289352069/pings",
                "last_response": {
                    "code": None,
                    "status": "unused",
                    "message": None
                }
            },
            "repository": {
                "id": 352990486,
                "node_id": "MDEwOlJlcG9zaXRvcnkzNTI5OTA0ODY=",
                "name": "lightweight-git-deployment",
                "full_name": "dolejska-daniel/lightweight-git-deployment",
                "private": True,
                "owner": {
                    "login": "dolejska-daniel",
                    "id": 10078080,
                    "node_id": "MDQ6VXNlcjEwMDc4MDgw",
                    "avatar_url": "https://avatars.githubusercontent.com/u/10078080?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/dolejska-daniel",
                    "html_url": "https://github.com/dolejska-daniel",
                    "followers_url": "https://api.github.com/users/dolejska-daniel/followers",
                    "following_url": "https://api.github.com/users/dolejska-daniel/following{/other_user}",
                    "gists_url": "https://api.github.com/users/dolejska-daniel/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/dolejska-daniel/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/dolejska-daniel/subscriptions",
                    "organizations_url": "https://api.github.com/users/dolejska-daniel/orgs",
                    "repos_url": "https://api.github.com/users/dolejska-daniel/repos",
                    "events_url": "https://api.github.com/users/dolejska-daniel/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/dolejska-daniel/received_events",
                    "type": "User",
                    "site_admin": False
                },
                "html_url": "https://github.com/dolejska-daniel/lightweight-git-deployment",
                "description": None,
                "fork": False,
                "url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment",
                "forks_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/forks",
                "keys_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/keys{/key_id}",
                "collaborators_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/collaborators{/collaborator}",
                "teams_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/teams",
                "hooks_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/hooks",
                "issue_events_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/issues/events{/number}",
                "events_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/events",
                "assignees_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/assignees{/user}",
                "branches_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/branches{/branch}",
                "tags_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/tags",
                "blobs_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/git/blobs{/sha}",
                "git_tags_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/git/tags{/sha}",
                "git_refs_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/git/refs{/sha}",
                "trees_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/git/trees{/sha}",
                "statuses_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/statuses/{sha}",
                "languages_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/languages",
                "stargazers_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/stargazers",
                "contributors_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/contributors",
                "subscribers_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/subscribers",
                "subscription_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/subscription",
                "commits_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/commits{/sha}",
                "git_commits_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/git/commits{/sha}",
                "comments_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/comments{/number}",
                "issue_comment_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/issues/comments{/number}",
                "contents_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/contents/{+path}",
                "compare_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/compare/{base}...{head}",
                "merges_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/merges",
                "archive_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/{archive_format}{/ref}",
                "downloads_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/downloads",
                "issues_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/issues{/number}",
                "pulls_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/pulls{/number}",
                "milestones_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/milestones{/number}",
                "notifications_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/notifications{?since,all,participating}",
                "labels_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/labels{/name}",
                "releases_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/releases{/id}",
                "deployments_url": "https://api.github.com/repos/dolejska-daniel/lightweight-git-deployment/deployments",
                "created_at": "2021-03-30T12:19:25Z",
                "updated_at": "2021-03-30T12:19:27Z",
                "pushed_at": "2021-03-30T12:19:25Z",
                "git_url": "git://github.com/dolejska-daniel/lightweight-git-deployment.git",
                "ssh_url": "git@github.com:dolejska-daniel/lightweight-git-deployment.git",
                "clone_url": "https://github.com/dolejska-daniel/lightweight-git-deployment.git",
                "svn_url": "https://github.com/dolejska-daniel/lightweight-git-deployment",
                "homepage": None,
                "size": 15,
                "stargazers_count": 0,
                "watchers_count": 0,
                "language": None,
                "has_issues": True,
                "has_projects": True,
                "has_downloads": True,
                "has_wiki": True,
                "has_pages": False,
                "forks_count": 0,
                "mirror_url": None,
                "archived": False,
                "disabled": False,
                "open_issues_count": 0,
                "license": {
                    "key": "gpl-3.0",
                    "name": "GNU General Public License v3.0",
                    "spdx_id": "GPL-3.0",
                    "url": "https://api.github.com/licenses/gpl-3.0",
                    "node_id": "MDc6TGljZW5zZTk="
                },
                "forks": 0,
                "open_issues": 0,
                "watchers": 0,
                "default_branch": "master"
            },
            "sender": {
                "login": "dolejska-daniel",
                "id": 10078080,
                "node_id": "MDQ6VXNlcjEwMDc4MDgw",
                "avatar_url": "https://avatars.githubusercontent.com/u/10078080?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/dolejska-daniel",
                "html_url": "https://github.com/dolejska-daniel",
                "followers_url": "https://api.github.com/users/dolejska-daniel/followers",
                "following_url": "https://api.github.com/users/dolejska-daniel/following{/other_user}",
                "gists_url": "https://api.github.com/users/dolejska-daniel/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/dolejska-daniel/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/dolejska-daniel/subscriptions",
                "organizations_url": "https://api.github.com/users/dolejska-daniel/orgs",
                "repos_url": "https://api.github.com/users/dolejska-daniel/repos",
                "events_url": "https://api.github.com/users/dolejska-daniel/events{/privacy}",
                "received_events_url": "https://api.github.com/users/dolejska-daniel/received_events",
                "type": "User",
                "site_admin": False
            }
    }

    dataclass_cls = dataclass_select_class_by_dict(event_classes, data)
    if dataclass_cls is None:
        raise HTTPBadRequest(reason="Unable to select dataclass corresponding to provided data.")

    dataclass = dataclass_from_dict(dataclass_cls, data)

    variables = {
        "request": request,
        "event": dataclass,
    }

    binding_data = AppConfig.get("bindings")[0]
    binding = dataclass_from_dict(EventBinding, binding_data)
    binding: EventBinding
    if binding.matches(dataclass):
        binding.run(variables)

    return Response(
        text="",
        status=HTTPAccepted.status_code
    )
