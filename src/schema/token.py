from .model import Object, datetime_pd, Field


class Token(Object):
    secret: str
    expires: datetime_pd = Field(description="Expiration date", validation_alias="expires_at")
