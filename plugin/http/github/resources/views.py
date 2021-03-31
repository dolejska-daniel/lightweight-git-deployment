import asyncio
import json
import logging
import hmac

from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPAccepted, HTTPBadRequest, HTTPUnsupportedMediaType, HTTPUnprocessableEntity

from deployer.config import AppConfig
from deployer.utils import dataclass_from_dict, dataclass_select_class_by_dict, dataclass_list_by_module
from deployer.utils.schemas import EventBinding

from .routes import routes
from .schemas import events

log = logging.getLogger("plugin.http.github")

event_classes = dataclass_list_by_module(events)


@routes.post("/github")
async def github_webhook_handler(request: Request):
    if (content_type := request.headers.get("Content-Type", "")) != "application/json":
        log.warning("received message with unsupported Content-Type=%s", content_type)
        raise HTTPUnsupportedMediaType(reason="Unable to process data of unsupported Content-Type.")

    data_raw = await request.text()
    data = dict(json.loads(data_raw))
    if key := AppConfig.get("github.secret"):
        digest_header_name = AppConfig.get("github.digest_header_name", "X-Hub-Signature-256")
        digest_method, digest_received = request.headers.get(digest_header_name, "sha256=").split("=", maxsplit=1)
        digest = hmac.digest(str(key).encode(), data_raw.encode(), digest_method).hex()
        if not hmac.compare_digest(digest, digest_received):
            raise HTTPUnprocessableEntity(reason="Refusing to process data with invalid signature.")

    log.log(0, "received content=%s", data)
    dataclass_cls = dataclass_select_class_by_dict(event_classes, data)
    if dataclass_cls is None:
        log.error("unable to find mapping for incomming message, content_keys=%s", list(data.keys()))
        raise HTTPBadRequest(reason="Unable to select dataclass corresponding to provided data.")

    dataclass = dataclass_from_dict(dataclass_cls, data)

    variables = {
        "request": request,
        "event_raw": data,
        "event": dataclass,
    }

    bindings = AppConfig.get("bindings")
    for _id, binding_data in enumerate(bindings):
        binding: EventBinding = dataclass_from_dict(EventBinding, binding_data)
        if binding.matches(dataclass):
            log.debug("binding %d matched, scheduling actions and continuing", _id)
            asyncio.create_task(binding.run(variables))

    return Response(
        text="",
        status=HTTPAccepted.status_code
    )
