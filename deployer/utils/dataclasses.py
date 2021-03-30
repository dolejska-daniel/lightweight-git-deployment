from dataclasses import dataclass, is_dataclass, fields, Field
from typing import Any, Type, Mapping, Union

dataclass_fields_cache = {}


def dataclass_from_dict(dataclass_cls: Type[dataclass],
                        data: Mapping[str, Any]
                        ) -> dataclass:
    dataclass_data = {**data}
    cls_fields = {field.name: field for field in fields(dataclass_cls)}
    for field_name in cls_fields:
        cls_field = cls_fields[field_name]  # type: Field
        if field_name not in data:
            dataclass_data[field_name] = None

        else:
            if is_dataclass(cls_field.type):
                dataclass_data[field_name] = dataclass_from_dict(cls_field.type, data[field_name])

            elif getattr(cls_field.type, "__origin__", None) == list:
                generic_class = getattr(cls_field.type, "__args__")[0]
                if is_dataclass(generic_class):
                    dataclass_data[field_name] = [dataclass_from_dict(generic_class, d) for d in data[field_name]]

    return dataclass_cls(**dataclass_data)


def dataclass_select_class_by_dict(dataclasses: list[dataclass],
                                   data: Mapping[str, Any]
                                   ) -> Union[dataclass, None]:
    data_fields = set(data.keys())
    for dataclass_cls in dataclasses:
        dataclass_fields = dataclass_fields_cache.get(dataclass_cls, {f.name for f in fields(dataclass_cls)})
        if data_fields.issubset(dataclass_fields):
            return dataclass_cls

    return None
