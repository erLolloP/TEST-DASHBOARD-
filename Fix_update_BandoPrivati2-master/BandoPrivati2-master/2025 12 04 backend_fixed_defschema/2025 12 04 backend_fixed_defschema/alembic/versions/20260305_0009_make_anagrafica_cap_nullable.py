from alembic import op
import sqlalchemy as sa


revision = "20260305_0009"
down_revision = "20260305_0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "items",
        "Anagrafica_cap",
        existing_type=sa.String(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "items",
        "Anagrafica_cap",
        existing_type=sa.String(),
        nullable=False,
    )
