import json
import logging
from typing import Union

from aiohttp import web

from deployer.config import AppConfig

log = logging.getLogger("deployer.http.server")
alog = logging.getLogger("deployer.http.server.access")


class Server(object):
    """ Class managing the application's control http. """

    def __init__(self):
        self._app = web.Application(logger=log)
        self._app.middlewares.append(self.error_middleware)
        self._runner = web.AppRunner(self._app, access_log=alog, access_log_format='"%r" %s %b %Tf "%{User-Agent}i"')
        self._site: Union[web.TCPSite, None] = None

    @classmethod
    @web.middleware
    async def error_middleware(cls, request, handler):
        from aiohttp.web_response import Response
        try:
            return await handler(request)

        except web.HTTPException as exc:
            return Response(text=json.dumps({
                "status": exc.status_code,
                "reason": exc.reason
            }), headers={"Content-Type": "application/json"}, status=exc.status_code)

        except Exception:
            log.exception("exception occured while processing API request")
            return Response(text=json.dumps({
                "status": 500,
                "reason": "Something went wrong. Check server log for more information",
            }), headers={"Content-Type": "application/json"}, status=500)

    # ==========================================================================dd==
    #   PUBLIC PROPERTIES
    # ==========================================================================dd==

    @property
    def app(self) -> web.Application:
        return self._app

    # ==========================================================================dd==
    #   PUBLIC METHODS
    # ==========================================================================dd==

    async def start(self):
        """ Starts the HTTP http. """
        server_config = AppConfig.get("http")
        log.debug("starting the HTTP http, using config=%s", server_config)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, **server_config)
        await self._site.start()
        log.debug("started the HTTP http")

    async def stop(self):
        """ Stops the HTTP http. """
        log.debug("stopping the HTTP http")
        await self._site.stop()
        log.debug("stopped the HTTP http")
