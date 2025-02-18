from src import util
from . import errors
from src.models import User
from fastapi.params import Depends
from src.route.service import get_user
from .schema import SigninSchema, SignupSchema
from src.session_holder import acquire_session
from sqlalchemy.ext.asyncio import AsyncSession


@util.fastapi.api_errors(errors.already_exists, errors.invalid_key)
async def validate_signup_schema(
    body: SignupSchema,
    session: AsyncSession = Depends(acquire_session),
) -> SignupSchema:
    user = await get_user(session, body.nickname)

    if user is not None:
        raise errors.already_exists

    try:
        util.cryptography.public_key_from_bytes(body.public_key)
    except ValueError:
        raise errors.invalid_key

    return body


@util.fastapi.api_errors(errors.invalid_secret, errors.no_user)
async def validate_signin_schema(
    body: SigninSchema,
    session: AsyncSession = Depends(acquire_session),
) -> User:
    user = await get_user(session, body.nickname)

    if user is None:
        raise errors.no_user

    if not util.secrets.verify(body.secret, user.secret_hash):
        raise errors.invalid_secret

    return user
