from typing import Any, Iterable

from pydantic import BeforeValidator


def convert_empty_str_to_none(value: Any) -> Any:
    if value == "" or (isinstance(value, Iterable) and all(s == "" for s in value)):  # type: ignore
        return None

    return value  # type: ignore


ConvertEmptyStrToNoneBeforeValidator = BeforeValidator(convert_empty_str_to_none)
