from tetra.plug import Multilingual, LogLevel, build
from tetra.plug.supply import Supply
from typing import Union, Optional, Mapping, Any
from deepdiff import DeepDiff


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
