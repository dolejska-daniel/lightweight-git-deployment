import asyncio
import logging

log = logging.getLogger("plugin.shell")


async def command(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    log.debug(stdout.decode().strip())
    if stderr:
        log.error(stderr.decode().strip())
