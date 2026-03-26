from alembic import op
import sqlalchemy as sa


revision = "20260305_0008"
down_revision = "20251118_0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "items",
        "Anagrafica_numeroSedi",
        existing_type=sa.Integer(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "items",
        "Anagrafica_numeroSedi",
        existing_type=sa.Integer(),
        nullable=False,
        existing_server_default=sa.text("0"),
    )
