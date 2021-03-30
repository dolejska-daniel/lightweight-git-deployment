import asyncio
import logging
import logging.config
from importlib import import_module
from types import ModuleType
from glob import glob

import yaml

from deployer.server import Server

log = logging.getLogger("deployer")


async def main():
    http = Server()

    log.debug("loading HTTP plugins")
    for module_dir_name in glob("plugin/http/*"):
        if module_dir_name.find("__") >= 0:
            # skip __pycache__
            continue

        module_name = module_dir_name.rstrip("\\/").replace("/", ".").replace("\\", ".")
        log.debug("loading module from '%s'", module_name)
        module: ModuleType = import_module(module_name)

        if not hasattr(module, "routes"):
            raise RuntimeError("Module '%s' does not contain route definition." % module_name)

        log.debug("registering module routes")
        http.app.add_routes(getattr(module, "routes"))

    await http.start()

    while True:
        await asyncio.sleep(5)


if __name__ == '__main__':
    with open("config/logging.yaml", "r") as fd:
        logging.config.dictConfig(yaml.safe_load(fd))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
