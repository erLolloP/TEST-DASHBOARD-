"""Relax NOT NULL on legacy columns no longer used by app

Revision ID: 20251118_0004
Revises: 20251118_0003
Create Date: 2025-11-18 00:30:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20251118_0004"
down_revision = "20251118_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rilassiamo il vincolo NOT NULL sulle vecchie colonne,
    # che non sono più usate dal codice ma esistono ancora nella tabella.
    with op.batch_alter_table("items") as batch:
        batch.alter_column(
            "structure_name",
            existing_type=sa.Text(),
            nullable=True,
        )
        batch.alter_column(
            "structure_code",
            existing_type=sa.Text(),
            nullable=True,
        )
        batch.alter_column(
            "p_iva",
            existing_type=sa.Text(),
            nullable=True,
        )
        batch.alter_column(
            "fornitore_name",
            existing_type=sa.Text(),
            nullable=True,
        )
        batch.alter_column(
            "software_name",
            existing_type=sa.Text(),
            nullable=True,
        )
        batch.alter_column(
            "software_version",
            existing_type=sa.Text(),
            nullable=True,
        )
        batch.alter_column(
            "software_docu_profile",
            existing_type=postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        )
        batch.alter_column(
            "convenzionato",
            existing_type=sa.Boolean(),
            nullable=True,
        )
        batch.alter_column(
            "accreditamento",
            existing_type=sa.Boolean(),
            nullable=True,
        )
        # asl_convenzionato e codice_regione_accreditamento sono già nullable=True in 0002,
        # quindi non serve toccarli.


def downgrade() -> None:
    # Ripristiniamo i vincoli NOT NULL come erano in 0002
    with op.batch_alter_table("items") as batch:
        batch.alter_column(
            "accreditamento",
            existing_type=sa.Boolean(),
            nullable=False,
        )
        batch.alter_column(
            "convenzionato",
            existing_type=sa.Boolean(),
            nullable=False,
        )
        batch.alter_column(
            "software_docu_profile",
            existing_type=postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        )
        batch.alter_column(
            "software_version",
            existing_type=sa.Text(),
            nullable=False,
        )
        batch.alter_column(
            "software_name",
            existing_type=sa.Text(),
            nullable=False,
        )
        batch.alter_column(
            "fornitore_name",
            existing_type=sa.Text(),
            nullable=False,
        )
        batch.alter_column(
            "p_iva",
            existing_type=sa.Text(),
            nullable=False,
        )
        batch.alter_column(
            "structure_code",
            existing_type=sa.Text(),
            nullable=False,
        )
        batch.alter_column(
            "structure_name",
            existing_type=sa.Text(),
            nullable=False,
        )
