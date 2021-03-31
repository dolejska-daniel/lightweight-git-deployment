import asyncio
import logging

from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPAccepted, HTTPBadRequest

from deployer.config import AppConfig
from deployer.utils import dataclass_from_dict, dataclass_select_class_by_dict, dataclass_list_by_module
from deployer.utils.schemas import EventBinding

from .routes import routes
from .schemas import events

log = logging.getLogger("plugin.http.github")

event_classes = dataclass_list_by_module(events)


@routes.get("/github")
async def github_webhook_handler(request: Request):
    if request.headers.get("Content-Type", "") == "application/json":
        data = dict(await request.json())

    else:
        data = dict(await request.post())

    dataclass_cls = dataclass_select_class_by_dict(event_classes, data)
    if dataclass_cls is None:
        log.warning("unable to find mapping for incomming message, content=%s", data)
        raise HTTPBadRequest(reason="Unable to select dataclass corresponding to provided data.")

    dataclass = dataclass_from_dict(dataclass_cls, data)

    variables = {
        "request": request,
        "event": dataclass,
    }

    bindings = AppConfig.get("bindings")
    for _id, binding_data in enumerate(bindings):
        binding: EventBinding = dataclass_from_dict(EventBinding, binding_data)
        if binding.matches(dataclass):
            log.debug("binding %d matched, running actions", _id)
            asyncio.create_task(binding.run(variables))

    return Response(
        text="",
        status=HTTPAccepted.status_code
    )
