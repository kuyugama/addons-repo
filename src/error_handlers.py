import fastapi

from src import error, errors, util


def error_handler(_, exc: error.APIError):
    return exc.response


async def default_handler(scope, receive, send):
    await errors.endpoint_not_found(extra=scope).response(scope, receive, send)


def validation_error_handler(_: fastapi.Request, exc: fastapi.exceptions.RequestValidationError):
    formatted_error = util.pydantic.format_error(exc)

    return fastapi.responses.JSONResponse(
        formatted_error,
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
