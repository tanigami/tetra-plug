"""Top-level package for Tetra Plug."""


from . import validators
from .supply import Supply

__author__ = """Hirofumi Tanigami"""
__email__ = "hirofumi.tanigami@shippinno.co.jp"
__version__ = "0.1.3"

__all__ = ["validators", "Supply"]


from typing import Dict, Literal


Locale = Literal["ja", "en"]
Multilingual = Dict[Locale, str]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


__all__ = ["validators", "Supply"]