from pydantic import Base64Bytes
from src.schema.model import Schema, Field


class SigninSchema(Schema):
    nickname: str = Field(
        min_length=3, max_length=16, pattern="[a-zA-Z0-9_]+", description="Nickname"
    )
    secret: str = Field(min_length=8, max_length=64, description="Secret")


class SignupSchema(Schema):
    nickname: str = Field(
        min_length=3, max_length=16, pattern="[a-zA-Z0-9_]+", description="Nickname"
    )
    secret: str = Field(min_length=8, max_length=64, description="Secret")

    public_key: Base64Bytes | None = Field(
        min_length=8,
        max_length=4096,
        description="Base64 encoded rsa public key",
    )
