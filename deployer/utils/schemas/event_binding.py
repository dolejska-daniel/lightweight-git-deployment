import asyncio
import logging
import re
from dataclasses import dataclass, asdict
from importlib import import_module
from typing import Optional, Any, overload, Mapping

from ..itertools import get_key_recursive

log = logging.getLogger("deployer.utils.schemas.event_binding")


@dataclass()
class EventBindingAction:
    call: str
    args: Optional[list[Any]]
    kwargs: Optional[dict[str, Any]]

    async def run(self, variables: dict[str, Any]):
        def prepare_arg(arg: Any) -> Any:
            if isinstance(arg, str) and arg.startswith("$"):
                if arg.find(".") >= 0:
                    variable_name, keys = arg[1:].split(".", maxsplit=1)
                    return get_key_recursive(variables[variable_name], keys, ".")

                else:
                    return variables[arg[1:]]

            elif isinstance(arg, str) and arg.startswith(";"):
                return eval(arg[1:], {}, variables)

            return arg

        module_name, method_name = self.call.rsplit(".", maxsplit=1)
        module = import_module(module_name)
        method = getattr(module, method_name)
        args = [prepare_arg(a) for a in self.args]
        kwargs = {k: prepare_arg(v) for k, v in self.kwargs.items()}

        if asyncio.iscoroutinefunction(method):
            await method(*args, **kwargs)

        else:
            method(*args, **kwargs)


@dataclass()
class EventBinding:
    conditions: list[dict[str, Any]]
    actions: list[EventBindingAction]

    @overload
    def matches(self, event: dataclass) -> bool:
        return self.matches(asdict(event))

    def matches(self, event: Mapping[str, Any]) -> bool:
        if not self.conditions:
            return True

        def conditions_and(conditions: dict[str, Any]):
            for condition_field, condition_value in conditions.items():
                try:
                    field_value = get_key_recursive(event, condition_field, ".")
                    if field_value != condition_value \
                            and (not isinstance(condition_value, str)
                                 or re.match(condition_value, field_value) is None):
                        return False

                except Exception:
                    log.exception("exception occured while trying to match %s with %s, field %s",
                                  condition_value, locals().get("field_value", None), condition_field)
                    return False

            return True

        for subconditions in self.conditions:
            if conditions_and(subconditions):
                return True

        return False

    async def run(self, variables: dict[str, Any]):
        for action in self.actions:
            await action.run(variables)
