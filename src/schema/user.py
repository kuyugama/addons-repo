from .model import Object, Field


class User(Object):
    nickname: str = Field(description="User nickname")
