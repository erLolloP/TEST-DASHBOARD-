
"""Split global certificate fields into domain-specific ones (LDO/LAB/RAD/RSA/RPA)

Revision ID: REVISION_PLACEHOLDER
Revises: DOWN_REVISION_PLACEHOLDER
Create Date: 2025-11-18 00:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251118_0005"
down_revision = "20251118_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Rimuovo i vecchi campi globali
    with op.batch_alter_table("items") as batch:
        for col in [
            "CN_Certificato",
            "richiesta_adesione",
            "ticket_cart",
            "referente_adesione",
            "referente_tecnico_applicativo",
            "test_case_1",
            "test_case_2",
            "test_case_3",
            "test_case_4",
            "data_richiesta_certificato",
            "data_emissione_certificato",
            "estar_autorizzazione_prod",
            "data_invio_certificati_ente_adesione",
            "data_accreditamento",
            "data_autorizzazione_rt_passaggio_in_produzione",
            "psw_certificato_raki",
        ]:
            try:
                batch.drop_column(col)
            except Exception:
                # in caso la colonna non esista (es. ambiente già parzialmente migrato),
                # ignoro per rendere la migration idempotente
                pass

    # 2) Creo i nuovi campi per ogni dominio (LDO/LAB/RAD/RSA/RPA)
    for prefix in ["LDO", "LAB", "RAD", "RSA", "RPA"]:
        op.add_column(
            "items",
            sa.Column(f"{prefix}_CN_Certificato", sa.String(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_richiesta_adesione", sa.Date(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_ticket_cart", sa.String(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_referente_adesione", sa.String(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(
                f"{prefix}_referente_tecnico_applicativo",
                sa.String(),
                nullable=True,
            ),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_test_validate_create", sa.Boolean(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_test_sostituzione", sa.Boolean(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_test_aggiornamento", sa.Boolean(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_test_eliminazione", sa.Boolean(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(
                f"{prefix}_data_richiesta_certificato",
                sa.Date(),
                nullable=True,
            ),
        )
        op.add_column(
            "items",
            sa.Column(
                f"{prefix}_data_emissione_certificato",
                sa.Date(),
                nullable=True,
            ),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_autorizzazione_prod", sa.Boolean(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(
                f"{prefix}_data_invio_certificati_ente_adesione",
                sa.Date(),
                nullable=True,
            ),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_data_accreditamento", sa.Date(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_data_autorizzazione_prod", sa.Date(), nullable=True),
        )
        op.add_column(
            "items",
            sa.Column(f"{prefix}_psw_certificato_raki", sa.String(), nullable=True),
        )


def downgrade() -> None:
    # Rimuovo i nuovi campi per dominio
    for prefix in ["LDO", "LAB", "RAD", "RSA", "RPA"]:
        for col_suffix in [
            "psw_certificato_raki",
            "data_autorizzazione_prod",
            "data_accreditamento",
            "data_invio_certificati_ente_adesione",
            "autorizzazione_prod",
            "data_emissione_certificato",
            "data_richiesta_certificato",
            "test_eliminazione",
            "test_aggiornamento",
            "test_sostituzione",
            "test_validate_create",
            "referente_tecnico_applicativo",
            "referente_adesione",
            "ticket_cart",
            "richiesta_adesione",
            "CN_Certificato",
        ]:
            col_name = f"{prefix}_{col_suffix}"
            try:
                op.drop_column("items", col_name)
            except Exception:
                pass

    # Ricreo i vecchi campi globali (nullable=True per evitare problemi su dati esistenti)
    with op.batch_alter_table("items") as batch:
        batch.add_column(sa.Column("CN_Certificato", sa.String(), nullable=True))
        batch.add_column(sa.Column("richiesta_adesione", sa.Date(), nullable=True))
        batch.add_column(sa.Column("ticket_cart", sa.String(), nullable=True))
        batch.add_column(sa.Column("referente_adesione", sa.String(), nullable=True))
        batch.add_column(sa.Column("referente_tecnico_applicativo", sa.String(), nullable=True))
        batch.add_column(sa.Column("test_case_1", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("test_case_2", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("test_case_3", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("test_case_4", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("data_richiesta_certificato", sa.Date(), nullable=True))
        batch.add_column(sa.Column("data_emissione_certificato", sa.Date(), nullable=True))
        batch.add_column(sa.Column("estar_autorizzazione_prod", sa.Boolean(), nullable=True))
        batch.add_column(sa.Column("data_invio_certificati_ente_adesione", sa.Date(), nullable=True))
        batch.add_column(sa.Column("data_accreditamento", sa.Date(), nullable=True))
        batch.add_column(sa.Column("data_autorizzazione_rt_passaggio_in_produzione", sa.Date(), nullable=True))
        batch.add_column(sa.Column("psw_certificato_raki", sa.String(), nullable=True))
