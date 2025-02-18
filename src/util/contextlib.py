import typing
from contextlib import asynccontextmanager as _asynccontextmanager

P = typing.ParamSpec("P")
R = typing.TypeVar("R")


def async_context_manager(
    func: typing.Callable[P, typing.AsyncIterator[R]],
) -> typing.Callable[P, typing.AsyncContextManager[R]]:
    return _asynccontextmanager(func)
