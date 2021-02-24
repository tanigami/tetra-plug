from typing import Callable, Optional, Sequence, Tuple, Union

from pfun.functions import curry

from .. import Multilingual, Supply


def message() -> Multilingual:
    return {"ja": "この項目は正しくありません。", "en": "Wrong value."}


@curry
def validate(
    input_, options: Union[Sequence, Callable], tetra: Supply, damup=True
) -> Tuple[Optional[Multilingual], str, bool]:
    error = (
        message()
        if input_ not in (options(tetra) if callable(options) else options)
        else None
    )
    return error, input_, damup
