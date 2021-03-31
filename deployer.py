import asyncio
import os
import logging.config
from importlib import import_module
from types import ModuleType
from glob import glob

import yaml

from deployer.http import Server

log = logging.getLogger("deployer")


async def main():
    with open("config/logging.yaml", "r") as fd:
        logging.config.dictConfig(yaml.safe_load(fd))

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
    pid_filepath = "deployer.pid"

    if os.path.exists(pid_filepath):
        raise RuntimeError("PID file already exists, refusing to start!")

    try:
        with open(pid_filepath, "w") as _pid_fd:
            _pid_fd.write(str(os.getpid()))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

    except Exception:
        log.exception("program encountered unrecoverable error, shutting down")

    finally:
        if os.path.exists(pid_filepath):
            os.remove(pid_filepath)
