from typing import Callable, Mapping, Optional, Sequence, Tuple, Union

from pfun.functions import curry

from . import Multilingual
from .supply import Supply

Result = Tuple[Optional[Mapping], str]


@curry
def required(input_: str, tetra: Supply) -> Result:
    error = (
        {
            "code": "REQUIRED",
            "message": {"ja": "この項目は必須です。", "en": "This field is reuired."},
        }
        if len(input_) == 0
        else None
    )
    return error, input_


@curry
def option(input_, options: Union[Sequence, Callable], tetra: Supply) -> Result:
    error = (
        {
            "code": "REQUIRED",
            "message": {"ja": "この項目は必須", "en": "This field is reuired"},
        }
        if input_ not in (options(tetra) if callable(options) else options)
        else None
    )
    return error, input_


@curry
def connection(input_: str, type: str, tetra: Supply) -> Result:
    error = (
        {
            "code": "CONNECTION_NOT_FOUND",
            "message": {"ja": "コネクションがありません。", "en": "Connection not found"},
        }
        if input_
        not in (connection["id"] for connection in tetra.get_connections(code=type))
        else None
    )
    return error, input_
