from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20251118_0007"
down_revision = "20251118_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "access_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("auth_time", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("fiscal_number", sa.String(), nullable=True),
        sa.Column("preferred_username", sa.String(), nullable=True),
        sa.Column("auth_type", sa.String(), nullable=False),
        sa.Column("auth_level", sa.String(), nullable=False),
        sa.Column("sid", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index("ix_access_logs_auth_time", "access_logs", ["auth_time"])
    op.create_index("ix_access_logs_sid", "access_logs", ["sid"])


def downgrade() -> None:
    op.drop_index("ix_access_logs_sid", table_name="access_logs")
    op.drop_index("ix_access_logs_auth_time", table_name="access_logs")
    op.drop_table("access_logs")
