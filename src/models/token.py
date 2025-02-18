from sqlalchemy import orm, ForeignKey
from datetime import datetime, timedelta

from src import util
from .user import User
from .base import Base


class Token(Base, table="service_tokens"):
    body: orm.Mapped[str] = orm.mapped_column(index=True, unique=True)

    owner_id = orm.mapped_column(ForeignKey(User.id))
    owner: orm.Mapped[User] = orm.relationship(foreign_keys=[owner_id])

    expires_at: orm.Mapped[datetime] = orm.mapped_column(
        default=lambda: util.datetime.now() + timedelta(seconds=util.token_ttl())
    )

    @property
    def secret(self):
        return self.body

    def prolong(self):
        self.expires_at = util.datetime.now() + timedelta(seconds=util.token_ttl())
