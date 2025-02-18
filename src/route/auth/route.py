from . import service
from src import schema
from src.models import User
from fastapi import APIRouter
from .schema import SignupSchema
from fastapi.params import Depends
from src.session_holder import acquire_session
from sqlalchemy.ext.asyncio import AsyncSession
from .dependencies import validate_signin_schema, validate_signup_schema


router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=schema.Token)
async def signup(
    body: SignupSchema = Depends(validate_signup_schema),
    session: AsyncSession = Depends(acquire_session),
):
    user = await service.create_user(session, body)

    return await service.create_token(session, user)


@router.post("/signin", response_model=schema.Token)
async def login(
    user: User = Depends(validate_signin_schema),
    session: AsyncSession = Depends(acquire_session),
):
    return await service.create_token(session, user)
