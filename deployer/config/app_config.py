from os import getenv
from typing import Any, Mapping

import yaml
from schema import Schema, Optional, Or


class AppConfig(object):

    _instance: "AppConfig" = None

    schema = Schema({
        Optional("http"): Schema({
            Optional("host", default="127.0.0.1"): str,
            Optional("port", default=8080): int,
            Optional("backlog"): int,
            Optional("reuse_address"): bool,
            Optional("reuse_port"): bool,
        }),

        Optional("bindings"): Schema([Schema({
            Optional("conditions"): Schema([Schema({
                Optional(object): Or(str, int, float, bool),
            })]),

            Optional("actions"): Schema([Schema({
                "call": str,
                Optional("args", default=list): Schema([object]),
                Optional("kwargs", default=dict): Schema({Optional(str): object}),
            })]),
        })]),
    })

    def __init__(self):
        with open(getenv("APP_CONFIG", "config/app.yaml"), "r") as fd:
            config = yaml.load(fd, Loader=yaml.FullLoader)

        self.config = self.schema.validate(config)

    @staticmethod
    def _get(value: Mapping[str, Any], name: str, default: Any = None) -> Any:
        from deployer.utils import get_key_recursive
        return get_key_recursive(value, name, ".", default=default)

    @classmethod
    def get(cls, name: str, default: Any = None) -> Any:
        if cls._instance is None:
            cls._instance = cls()

        return cls._get(cls._instance.config, name, default)
