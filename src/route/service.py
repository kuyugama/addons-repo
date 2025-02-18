from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import User, Token


async def get_user(session: AsyncSession, nickname: str) -> User | None:
    return await session.scalar(select(User).filter_by(nickname=nickname))


async def get_token(session: AsyncSession, token_body: str) -> Token:
    return await session.scalar(
        select(Token).filter_by(body=token_body).options(joinedload(Token.owner))
    )
