"""initial

Revision ID: a02c851ebd8c
Revises:
Create Date: 2025-02-04 08:42:19.892575

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a02c851ebd8c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "service_users",
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("secret_hash", sa.String(), nullable=False),
        sa.Column("public_key", sa.LargeBinary(), nullable=False),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_service_users_created_at"), "service_users", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_service_users_id"), "service_users", ["id"], unique=False)
    op.create_index(op.f("ix_service_users_nickname"), "service_users", ["nickname"], unique=False)
    op.create_index(
        op.f("ix_service_users_updated_at"), "service_users", ["updated_at"], unique=False
    )
    op.create_table(
        "service_addons",
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("meta", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("encrypted", sa.Boolean(), nullable=True),
        sa.Column("secret", sa.LargeBinary(), nullable=True),
        sa.Column("owner_id", sa.BIGINT(), nullable=True),
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["service_users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_service_addons_created_at"), "service_addons", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_service_addons_id"), "service_addons", ["id"], unique=False)
    op.create_index(
        op.f("ix_service_addons_updated_at"), "service_addons", ["updated_at"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_service_addons_updated_at"), table_name="service_addons")
    op.drop_index(op.f("ix_service_addons_id"), table_name="service_addons")
    op.drop_index(op.f("ix_service_addons_created_at"), table_name="service_addons")
    op.drop_table("service_addons")
    op.drop_index(op.f("ix_service_users_updated_at"), table_name="service_users")
    op.drop_index(op.f("ix_service_users_nickname"), table_name="service_users")
    op.drop_index(op.f("ix_service_users_id"), table_name="service_users")
    op.drop_index(op.f("ix_service_users_created_at"), table_name="service_users")
    op.drop_table("service_users")
    # ### end Alembic commands ###
