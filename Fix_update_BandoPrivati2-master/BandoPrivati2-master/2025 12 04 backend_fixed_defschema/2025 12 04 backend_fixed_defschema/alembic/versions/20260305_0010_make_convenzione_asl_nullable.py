from alembic import op
import sqlalchemy as sa


revision = "20260305_0010"
down_revision = "20260305_0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "items",
        "Anagrafica_convenzioneASL",
        existing_type=sa.Boolean(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "items",
        "Anagrafica_convenzioneASL",
        existing_type=sa.Boolean(),
        nullable=False,
    )
