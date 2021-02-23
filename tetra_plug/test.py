from . import Multilingual, LogLevel
from .supply import Supply
from typing import Union, Optional, Mapping, Any


class TestSupply(Supply):
    testing = True

    def __init__(self, inputs, connections=[]):
        self.inputs = inputs
        self.connections = connections
        self.logs = []
        self.halted = False
        self.echoes = {}

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
        self.halted = True

    def resolve_input(self, field_key: str):
        print(1)

    def echo(self, key: str, value: Any) -> None:
        self.echoes[key] = value


def test_note(module):
    test_validate(module)
    test_play(module)


def test_validate(module):
    specs = module.specs.validate
    for spec in specs:
        supply = TestSupply(inputs=spec["inputs"], connections=spec["connections"])
        state = build(inputs=spec["inputs"], fields=module.fields, tetra=supply)
        diff = DeepDiff(state, spec["state"])
        print(diff)
        # print("diff", DeepDiff(state, spec["state"]))
        # assert "values_changed" not in diff and "dictionary_item_added" not in diff
        assert state == spec["state"]
        print(".")


def test_play(module):
    specs = module.specs.play
    for spec in specs:
        supply = TestSupply(inputs=spec["inputs"], connections=spec["connections"])
        module.play(tetra=supply)
        print(supply.logs)
        # assert supply.logs == spec["logs"]
        assert supply.halted == spec.get("halted", False)
        print(supply.echoes)
        assert supply.echoes == spec["echoes"]
        print(".")


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
