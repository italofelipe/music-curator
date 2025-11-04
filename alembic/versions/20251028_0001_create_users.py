from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20251028_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Sobe a migração que cria a tabela de usuários.
    """
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id", name="pk_users_id"),
    )
    op.create_unique_constraint("uq_users_email", "users", ["email"])


def downgrade() -> None:
    """
    Reverte a criação da tabela de usuários.
    """
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.drop_table("users")
