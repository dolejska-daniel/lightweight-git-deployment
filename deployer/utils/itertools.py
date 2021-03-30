from collections import Mapping
from dataclasses import is_dataclass
from typing import Any


def get_key_recursive(value: Mapping[str, Any], name: str, splitter: str = ".", default: Any = None) -> Any:
    for key in name.split(splitter):
        if isinstance(value, list):
            value = value[int(key)]
            continue

        elif is_dataclass(value):
            value = getattr(value, key)
            continue

        elif not isinstance(value, Mapping):
            raise RuntimeError(
                "Failed to extract provided key %s. Entry at '%s' is of type %s."
                % (name, key, str(type(value)))
            )

        value = value.get(key, default)

    return value
