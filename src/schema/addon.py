from . import User
from .model import Object, Field, Schema


class Addon(Object):
    id: str = Field(
        validation_alias="addon_id", description="Hash of the addon id specified in metadata"
    )
    name: str
    authors: list[str]
    description: str
    depends: list[str]
    owner: User


class AddonVersion(Schema):
    version: str
    encrypted: bool
    secret: str | None = Field(description="Base64-encoded rsa-encrypted addon encryption key")


class AddonWithVersions(Addon):
    versions: list[AddonVersion]
