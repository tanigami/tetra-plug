from typing import TypedDict, Optional
from datetime import datetime, date
from os import environ
from functools import wraps
from tetra.plug.supply import Supply
import json


class OAuth2Credentials(TypedDict):
    access_token: str
    access_token_expires_at: Optional[datetime]
    refresh_token: Optional[str]
    refresh_token_expires_at: Optional[datetime]


def get_client_id(code: str) -> str:
    return environ.get(f"{code.upper()}_OAUTH2_CLIENT_ID", "")


def get_client_secret(code: str) -> str:
    return environ.get(f"{code.upper()}_OAUTH2_CLIENT_SECRET", "")


def get_redirect_uri(code: str) -> str:
    return environ.get(f"{code.upper()}_OAUTH2_REDIRECT_URI", "")


def logged(action, reference, ok, ng):
    def decorator(f):
        @wraps(f)
        def wrapper(tetra: Supply, *args, **kwds):
            response, request = f(tetra=tetra, *args, **kwds)
            context = {
                "api": {
                    "request": json.dumps(
                        request,
                        ensure_ascii=False,
                        default=lambda obj: (
                            obj.isoformat()
                            if isinstance(obj, (datetime, date))
                            else None
                        ),
                    ),
                    "response": json.dumps(
                        response,
                        ensure_ascii=False,
                        default=lambda obj: (
                            obj.isoformat()
                            if isinstance(obj, (datetime, date))
                            else None
                        ),
                    ),
                },
            }
            if ok(response=response):
                tetra.log(
                    level="INFO",
                    message=f"{action} - OK",
                    context=context,
                )
                error = False
            else:
                message, code = ng(response)
                message = f"{action} - {message}"
                if code is not None:
                    message = f"{message} ({code})"
                tetra.log(
                    level="WARNING",
                    message=message,
                    context=context,
                )
                error = True
            return response, error

        return wrapper

    return decorator