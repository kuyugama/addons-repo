from sqlalchemy import orm
from functools import lru_cache
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from .. import util
from .base import Base


class User(Base, table="service_users"):
    nickname: orm.Mapped[str] = orm.mapped_column(index=True)
    secret_hash: orm.Mapped[str]
    public_key: orm.Mapped[bytes]

    addons: orm.Mapped[int] = orm.mapped_column(server_default="0")

    @property
    @lru_cache
    def python_public_key(self) -> RSAPublicKey:
        return util.cryptography.public_key_from_bytes(self.public_key)

    def encrypt(self, data: bytes) -> bytes:
        return util.cryptography.rsa_encrypt(self.python_public_key, data)
