import json
import logging
from datetime import datetime

from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPOk

from plugin.git import describe

from .routes import routes

log = logging.getLogger("plugin.http.default")

started_at = datetime.now()


@routes.get("/")
async def default_handler(*_):
    data = {
        "version": describe("."),
        "uptime": str(datetime.now() - started_at),
    }

    return Response(
        text=json.dumps(data),
        status=HTTPOk.status_code
    )
