import re
import math
import typing
from src import constants
from dynaconf import Dynaconf
from functools import lru_cache
from sqlalchemy.orm import DeclarativeBase
from . import datetime, secrets, string, contextlib, fastapi, pydantic, cryptography


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.yaml", ".secrets.yaml"],
)


def get_offset_and_limit(page: int, size: int = constants.misc.DEFAULT_PAGE_SIZE):
    return (page - 1) * size, size


def paginated_response(
    items: typing.Sequence[DeclarativeBase],
    total: int,
    offset: int,
    limit: int,
):
    return {
        "items": items,
        "pagination": {
            "total": total,
            "page": (offset / limit) + 1,
            "pages": math.ceil(total / limit),
        },
    }


@lru_cache
def token_ttl() -> int:
    raw_ttl = settings.token.ttl.replace(" ", "")
    if re.match(r"[1-9][0-9*]+", raw_ttl) is None:
        raise RuntimeError(
            'Cannot parse token ttl expression: must match the format "[1-9][0-9*]+" where * is multiply symbol'
        )

    return eval(raw_ttl, {}, {})


token_ttl()
