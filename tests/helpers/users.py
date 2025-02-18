import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, Token


async def create_user(session: AsyncSession, nickname: str, secret_hash: str, public_key: bytes):
    user = User(
        nickname=nickname,
        secret_hash=secret_hash,
        public_key=public_key,
    )
    session.add(user)

    await session.commit()

    return user


async def create_token(session: AsyncSession, user: User):
    token = Token(body=secrets.token_hex(16), owner=user)
    session.add(token)

    await session.commit()

    return token
