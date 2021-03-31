from dataclasses import dataclass, is_dataclass, fields, Field
from types import ModuleType
from typing import Any, Type, Mapping, Union
import logging

log = logging.getLogger("deployer.utils.dataclasses")

dataclass_fields_cache = {}


def _get_dataclass_fields(dataclass_cls: Type[dataclass]) -> dict[str, Field]:
    if dataclass_cls not in dataclass_fields_cache:
        dataclass_fields_cache[dataclass_cls] = {f.name for f in fields(dataclass_cls)}

    return dataclass_fields_cache[dataclass_cls]


def dataclass_from_dict(dataclass_cls: Type[dataclass],
                        data: Mapping[str, Any]
                        ) -> dataclass:
    if not data:
        return None

    dataclass_data = {**data}
    cls_fields = _get_dataclass_fields(dataclass_cls)
    for field_name in cls_fields:
        cls_field = cls_fields[field_name]  # type: Field
        if field_name not in data:
            dataclass_data[field_name] = None

        else:
            try:
                if is_dataclass(cls_field.type):
                    dataclass_data[field_name] = dataclass_from_dict(cls_field.type, data[field_name])

                elif getattr(cls_field.type, "__origin__", None) == list:
                    generic_class = getattr(cls_field.type, "__args__")[0]
                    if is_dataclass(generic_class):
                        dataclass_data[field_name] = [dataclass_from_dict(generic_class, d) for d in data[field_name]]

            except TypeError as ex:
                raise RuntimeError(
                    "failed instantiating %s at '%s' key"
                    % (cls_field.type.__name__, field_name)
                ) from ex

    return dataclass_cls(**dataclass_data)


def dataclass_select_class_by_dict(dataclasses: list[dataclass],
                                   data: Mapping[str, Any]
                                   ) -> Union[dataclass, None]:
    data_fields = set(data.keys())
    for dataclass_cls in dataclasses:
        dataclass_fields = set(_get_dataclass_fields(dataclass_cls).keys())
        if data_fields.issubset(dataclass_fields):
            log.debug("provided data with fields %s matched %s", data_fields, dataclass_cls)
            return dataclass_cls

    log.warning("provided data with fields %s matched no dataclasses", data_fields)
    return None


def dataclass_list_by_module(module: ModuleType) -> list[dataclass]:
    classes = [getattr(module, cls_name, None) for cls_name in dir(module)]
    return list(filter(lambda cls: is_dataclass(cls), classes))
