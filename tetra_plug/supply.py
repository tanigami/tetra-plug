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

from pfun.functions import curry
import abc

# from tetra.plug import Connection

ConnectionFieldKey = str
FieldKey = str

Locale = Literal["ja", "en"]

Multilingual = Dict[Locale, str]

MultilingualOrString = Union[Multilingual, str]

GetConnection = Callable[[ConnectionFieldKey], Any]
GetInput = Callable[[FieldKey], Any]


LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]
LogMessage = MultilingualOrString
Log = Callable[[LogLevel, LogMessage], None]

Halt = Callable[[LogMessage], None]


class Fields(abc.ABC):
    @curry
    def text(
        self,
        key: str,
        label: Union[Multilingual, str],
        multiline: bool,
        validators,
        depends_on: Optional[str] = None,
    ):
        pass

    def select(
        self,
        key: str,
        label: Union[Multilingual, str],
        options: Callable[[], Dict[str, Mapping[str, str]]],
        depends_on: Optional[str] = None,
    ):
        pass

    def connection(
        self,
        key: str,
        label: Union[Multilingual, str],
        compatibles: Sequence[str] = None,
        depends_on: Optional[str] = None,
    ):
        pass

    def list(
        self,
        key: str,
        label: Union[Multilingual, str],
        item,
        depends_on: Optional[str] = None,
    ):
        pass


class Supply(abc.ABC):
    """[summary].

    Args:
        Protocol ([type]): [description]
    """

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

    fields: Fields