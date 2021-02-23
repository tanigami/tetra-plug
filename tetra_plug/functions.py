from typing import Callable, Any, Literal, TypedDict, Union

ConnectionFieldKey = str
FieldKey = str


class Multilingual(TypedDict):
    ja: str
    en: str


MultilingualOrString = Union[Multilingual, str]

GetConnection = Callable[[ConnectionFieldKey], Any]
GetInput = Callable[[FieldKey], Any]


LogLevel = Literal["DEBUG", "INFO", "ERROR"]
LogMessage = MultilingualOrString
Log = Callable[[LogLevel, LogMessage], None]

Halt = Callable[[LogMessage], None]