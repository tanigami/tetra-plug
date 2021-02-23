"""Top-level package for Tetra Plug."""

__author__ = """Hirofumi Tanigami"""
__email__ = 'hirofumi.tanigami@shippinno.co.jp'
__version__ = '0.1.0'


from tetra.plug.supply import Supply
from typing import (
    Callable,
    Any,
    Dict,
    Literal,
    Mapping,
    Optional,
    OrderedDict,
    Sequence,
    TypedDict,
    Union,
)

from pfun.functions import A, curry
import abc

# from tetra.plug import Connection

ConnectionFieldKey = str
FieldKey = str

Locale = Literal["ja", "en"]

Multilingual = Dict[Locale, str]

MultilingualOrString = Union[Multilingual, str]

GetConnection = Callable[[ConnectionFieldKey], Any]
GetInput = Callable[[FieldKey], Any]


LogLevel = Literal["DEBUG", "INFO", "ERROR"]
LogMessage = MultilingualOrString
Log = Callable[[LogLevel, LogMessage], None]

Halt = Callable[[LogMessage], None]


@curry
def build(inputs, fields, tetra: Supply):
    from .validators import option, connection

    # state = OrderedDict()
    print("INPUT", inputs)
    state = {}
    for field in fields():
        if "depends_on" in field and not field["depends_on"](state=state):
            continue
        if field["key"] not in inputs:
            inputs[field["key"]] = None
        if inputs[field["key"]] is None:
            inputs[field["key"]] = field.get("default", None)
        state[field["key"]] = validate(inputs[field["key"]], field, tetra, state)
    return state


def validate(input_, field, tetra, state):
    from .validators import option, connection

    print("VALIDATE", input_)
    if field["type"] == "list":
        return {
            "fields": {
                key: validate(i, field["item"], tetra, state)
                for key, i in (input_.items() if input_ != [] else {})
            }
            if input_ is not None
            else {},
            "errors": [],
        }

    if input_ is None:
        return {"input": input_, "errors": []}

    elif field["type"] == "group":
        return {
            k: validate(
                v, next(f for f in field["items"] if f["key"] == k), tetra, state
            )
            for k, v in input_.items()
        }
    else:
        if input_ is not None:
            # if field["type"] == "connection":
            #     field["validators"] = field["validators"] + [
            #         connection(type="google_maps")
            #     ]
            if field["type"] == "select":
                field["validators"] = (
                    option(options=field["options"](tetra=tetra), tetra=tetra),
                )
        errors = (
            lambda: [
                error
                for validator in field["validators"]
                if (error := validator(input_=input_, tetra=tetra)[0]) is not None
            ]
            if "validators" in field
            else []
        )
        return {
            "input": input_,
            "errors": errors,
        }
