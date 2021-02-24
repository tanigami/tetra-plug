import abc
from typing import Any, Mapping, Optional, Sequence, Union
from . import LogLevel, Multilingual


class Supply(abc.ABC):
    testing = False

    @abc.abstractmethod
    def get_input(self, field_key: str) -> Any:
        pass

    @abc.abstractmethod
    def get_connection(self, field_key: str):
        pass

    @abc.abstractmethod
    def get_connections(self, code: str) -> Sequence:
        pass

    @abc.abstractmethod
    def log(
        self,
        level: LogLevel,
        message: Union[str, Multilingual],
        context: Optional[Mapping[str, Any]] = None,
    ):
        pass

    @abc.abstractmethod
    def halt(self, message: Union[str, Multilingual]):
        pass

    @abc.abstractmethod
    def resolve_input(self, field_key: str):
        pass

    @abc.abstractmethod
    def echo(self, key: str, value: Any) -> None:
        pass
