from . import Multilingual, LogLevel, Supply
from typing import MutableMapping, Union, Optional, Mapping, Any, Sequence
import pytest
from pfun.functions import curry
from .validators import options


class HaltError(Exception):
    pass


class TestSupply(Supply):
    def __init__(
        self,
        inputs,
        connections: Optional[Sequence] = None,
        testing: Optional[Union[Mapping, bool]] = True,
    ):
        self.inputs = inputs
        self.connections = connections if connections is not None else []
        self.testing = testing
        self.logs = []
        self.echo: MutableMapping = {}

    def get_input(self, field_key: str):
        return self.inputs[field_key]

    def get_connection(self, field_key: str):
        return next(
            (
                connection
                for connection in self.connections
                if connection["id"] == self.get_input(field_key)
            ),
            None,
        )

    def get_connections(self, code: str):
        return self.connections

    def log(
        self,
        level: LogLevel,
        message: Union[str, Multilingual],
        context: Optional[Mapping[str, Any]] = None,
    ):
        self.logs.append({"level": level, "message": message, "context": context})

    def halt(self, message: Union[str, Multilingual]):
        self.logs.append({"level": "ERROR", "message": message})
        raise HaltError()

    def resolve_input(self, field_key: str):
        print(1)

    def leave_echo(self, key: str, value: Any) -> None:
        self.echo[key] = value


def test_tone(spec, tone):
    supply = TestSupply(inputs=spec["tone"], testing=spec.get("testing", True))
    state = emulate_state(tone=spec["tone"], fields=tone, tetra=supply)
    assert state == spec["state"]


def test_play(spec, play):
    supply = TestSupply(inputs=spec["tone"], testing=spec.get("testing", True))
    if spec.get("halted", False):
        with pytest.raises(HaltError):
            play(tetra=supply)
    else:
        play(tetra=supply)
    assert supply.logs == spec["logs"]
    assert supply.echo == spec["echo"]


@curry
def emulate_state(tone, fields, tetra: Supply):
    # tone = tone(tetra=tetra)
    state = {}
    for field in fields(tetra=tetra):
        if "depends_on" in field and not field["depends_on"](state=state):
            continue
        if field["key"] not in tone:
            tone[field["key"]] = None
        if tone[field["key"]] is None:
            tone[field["key"]] = field.get("default", None)
        state[field["key"]] = validate(tone[field["key"]], field, tetra, state)
    return state


def validate(input_, field, tetra, state):
    if input_ is None:
        return {"input": input_, "errors": []}
    if field["type"] == "select":
        field["validators"] = field["validators"] + [
            options.validate(options=field["options"](tetra=tetra), tetra=tetra)
        ]

    errors = []
    if "validators" in field:
        for validator in field["validators"]:
            error, input_, damup = validator(input_=input_, tetra=tetra)
            if error is not None:
                errors.append(error)
                if damup:
                    break
    return {
        "input": input_,
        "errors": errors,
    }

    # print("VALIDATE", input_)
    # if field["type"] == "list":
    #     return {
    #         "fields": {
    #             key: validate(i, field["item"], tetra, state)
    #             for key, i in (input_.items() if input_ != [] else {})
    #         }
    #         if input_ is not None
    #         else {},
    #         "errors": [],
    #     }

    # if input_ is None:
    #     return {"input": input_, "errors": []}

    # elif field["type"] == "group":
    #     return {
    #         k: validate(
    #             v, next(f for f in field["items"] if f["key"] == k), tetra, state
    #         )
    #         for k, v in input_.items()
    #     }
    # else:
    #     if input_ is not None:
    #         # if field["type"] == "connection":
    #         #     field["validators"] = field["validators"] + [
    #         #         connection(type="google_maps")
    #         #     ]
    #         if field["type"] == "select":
    #             field["validators"] = (
    #                 option(options=field["options"](tetra=tetra), tetra=tetra),
    #             )
    #     errors = (
    #         lambda: [
    #             error
    #             for validator in field["validators"]
    #             if (error := validator(input_=input_, tetra=tetra)[0]) is not None
    #         ]
    #         if "validators" in field
    #         else []
    #     )
    #     return {
    #         "input": input_,
    #         "errors": errors,
    #     }
