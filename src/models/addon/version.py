from sqlalchemy import orm, ForeignKey

from ..base import Base
from .addon import Addon


class AddonVersion(Base, table="service_addon_versions"):
    addon_id = orm.mapped_column(ForeignKey(Addon.id, ondelete="CASCADE"))
    addon: orm.Mapped[Addon] = orm.relationship(foreign_keys=[addon_id], back_populates="versions")

    version: orm.Mapped[str]
    path: orm.Mapped[str]

    encrypted: orm.Mapped[bool] = orm.mapped_column(default=False)
    # Secret have one purpose - decrypt addon. Secret is encrypted itself using user's public key
    secret: orm.Mapped[str] = orm.mapped_column(nullable=True)
