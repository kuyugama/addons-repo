import typing
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm.attributes import set_committed_value
from sqlalchemy import orm, ForeignKey, event, Connection, update, String

from ..base import Base
from ..user import User

if typing.TYPE_CHECKING:
    from .version import AddonVersion


class Addon(Base, table="service_addons"):
    addon_id: orm.Mapped[str] = orm.mapped_column(unique=True)
    name: orm.Mapped[str]
    description: orm.Mapped[str]
    depends: orm.Mapped[list[str]] = orm.mapped_column(ARRAY(String))
    authors: orm.Mapped[list[str]] = orm.mapped_column(ARRAY(String))

    versions: orm.Mapped[list["AddonVersion"]] = orm.relationship(
        uselist=True, back_populates="addon"
    )

    owner_id = orm.mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    owner: orm.Mapped[User] = orm.relationship(foreign_keys=[owner_id])


@event.listens_for(Addon, "before_insert")
def _new_addon(_: type[Addon], connection: Connection, addon: Addon):
    set_committed_value(addon.owner, "addons", addon.owner.addons + 1)
    connection.execute(update(User).values(addons=User.addons + 1).filter_by(id=addon.owner_id))


@event.listens_for(Addon, "before_delete")
def _remove_addon(_: type[Addon], connection: Connection, addon: Addon):
    set_committed_value(addon.owner, "addons", addon.owner.addons - 1)
    connection.execute(update(User).values(addons=User.addons - 1).filter_by(id=addon.owner_id))
