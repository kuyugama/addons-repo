from fastapi import Query, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Token
from src import constants, util
from src.route import service, errors
from src.session_holder import acquire_session


async def require_offset_and_limit(
    page: int = Query(1, ge=1),
    size: int = Query(constants.misc.DEFAULT_PAGE_SIZE, ge=1, le=constants.misc.MAX_PAGE_SIZE),
) -> tuple[int, int]:
    return util.get_offset_and_limit(page, size)


@util.fastapi.api_errors(errors.token_invalid, errors.token_expired)
async def require_token(
    token_body: str = Header(alias="X-Token"),
    session: AsyncSession = Depends(acquire_session),
):
    token = await service.get_token(session, token_body)

    if not token:
        raise errors.token_invalid

    if token.expires_at < util.datetime.now():
        raise errors.token_expired

    token.prolong()

    await session.commit()

    return token


async def require_user(token: Token = Depends(require_token)):
    return token.owner
