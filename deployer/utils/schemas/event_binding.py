import re
from dataclasses import dataclass, asdict
from importlib import import_module
from typing import Optional, Any, overload, Mapping

from .. import get_key_recursive


@dataclass()
class EventBindingAction:
    call: str
    args: Optional[list[Any]]
    kwargs: Optional[dict[str, Any]]

    def run(self, variables: dict[str, Any]):
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
        getattr(module, method_name)(
            *[prepare_arg(a) for a in self.args],
            **{k: prepare_arg(v) for k, v in self.kwargs.items()},
        )


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
                            and re.match(condition_value, field_value) is None:
                        return False

                except Exception:
                    return False

            return True

        for subconditions in self.conditions:
            if conditions_and(subconditions):
                return True

        return False

    def run(self, variables: dict[str, Any]):
        for action in self.actions:
            action.run(variables)
