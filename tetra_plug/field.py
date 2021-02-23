from typing import Union


from . import Multilingual
from typing import Union, Tuple, Optional, Mapping, Dict, Callable, Sequence
from pfun.functions import curry


@curry
def fulfilled(field_key: str, state: Mapping):
    return (
        state[field_key]["input"] is not None and len(state[field_key]["errors"]()) == 0
    )
