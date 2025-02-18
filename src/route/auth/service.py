import hashlib
import secrets
from src import util
from src.models import User, Token
from src.route.auth.schema import SignupSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(session: AsyncSession, body: SignupSchema) -> User:
    user = User(
        nickname=body.nickname,
        secret_hash=util.secrets.make(body.secret),
        public_key=body.public_key,
    )

    session.add(user)
    await session.commit()

    return user


async def create_token(session: AsyncSession, user: User) -> Token:
    user_hash = hashlib.sha256(user.nickname.encode()).hexdigest()
    token = Token(
        body=user_hash[16:] + secrets.token_hex(32) + user_hash[-16:],
        owner=user,
    )

    session.add(token)
    await session.commit()

    return token
