import logging
from typing import Union

from aiohttp import web

from deployer.config import AppConfig

log = logging.getLogger("deployer.http.server")


class Server(object):
    """ Class managing the application's control http. """

    def __init__(self):
        self._app = web.Application(logger=log)
        self._runner = web.AppRunner(self._app, access_log=log, access_log_format='"%r" %s %b %Tf "%{User-Agent}i"')
        self._site: Union[web.TCPSite, None] = None

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
