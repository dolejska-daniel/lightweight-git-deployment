import asyncio

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


@routes.post("/github")
async def github_webhook_handler(request: Request):
    if request.headers.get("Content-Type", "") == "application/json":
        data = dict(await request.json())

    else:
        data = dict(await request.post())

    dataclass_cls = dataclass_select_class_by_dict(event_classes, data)
    if dataclass_cls is None:
        raise HTTPBadRequest(reason="Unable to select dataclass corresponding to provided data.")

    dataclass = dataclass_from_dict(dataclass_cls, data)

    variables = {
        "request": request,
        "event": dataclass,
    }

    bindings = AppConfig.get("bindings")
    for binding_data in bindings:
        binding: EventBinding = dataclass_from_dict(EventBinding, binding_data)
        if binding.matches(dataclass):
            asyncio.create_task(binding.run(variables))

    return Response(
        text="",
        status=HTTPAccepted.status_code
    )
