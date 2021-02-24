from typing import Optional, Tuple

from pfun.functions import curry

from .. import Multilingual, Supply


def message() -> Multilingual:
    return {"ja": "この項目は必須です。", "en": "This field is reuired."}


@curry
def validate(
    input_: str, tetra: Supply, damup: bool = True
) -> Tuple[Optional[Multilingual], str, bool]:
    error = message() if len(input_) == 0 else None
    return error, input_, damup