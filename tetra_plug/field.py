from typing import Mapping
from pfun.functions import curry


@curry
def fulfilled(field_key: str, state: Mapping):
    return (
        state[field_key]["input"] is not None and len(state[field_key]["errors"]()) == 0
    )
