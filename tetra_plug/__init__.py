"""Top-level package for Tetra Plug."""
import abc
from typing import Any, Dict, Literal, Mapping, Optional, Sequence, Union

from . import validators

__author__ = """Hirofumi Tanigami"""
__email__ = "hirofumi.tanigami@shippinno.co.jp"
__version__ = "0.1.3"

__all__ = ["validators", "Supply"]


Locale = Literal["ja", "en"]
Multilingual = Dict[Locale, str]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


__all__ = ["validators", "Supply"]


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
    def leave_echo(self, key: str, value: Any) -> None:
        pass
