from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20251028_0002"
down_revision = "20251023_0001"
branch_labels = None
depends_on = None

def upgrade() -> None:
    with op.batch_alter_table("items") as batch:
        batch.drop_column("name")
        batch.drop_column("payload")

    op.add_column("items", sa.Column("structure_name", sa.Text(), nullable=False))
    op.add_column("items", sa.Column("structure_code", sa.Text(), nullable=False))
    op.add_column("items", sa.Column("p_iva", sa.Text(), nullable=False))
    op.add_column("items", sa.Column("fornitore_name", sa.Text(), nullable=False))
    op.add_column("items", sa.Column("software_name", sa.Text(), nullable=False))
    op.add_column("items", sa.Column("software_version", sa.Text(), nullable=False))
    op.add_column("items", sa.Column("software_docu_profile", postgresql.JSONB(astext_type=sa.Text()), server_default=sa.text("'[]'::jsonb"), nullable=False))
    op.add_column("items", sa.Column("convenzionato", sa.Boolean(), nullable=False))
    op.add_column("items", sa.Column("accreditamento", sa.Boolean(), nullable=False))
    op.add_column("items", sa.Column("asl_convenzionato", sa.Text(), nullable=True))
    op.add_column("items", sa.Column("codice_regione_accreditamento", sa.Text(), nullable=True))
    op.add_column("items", sa.Column("fornitore_name_check", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("software_name_check", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("software_version_check", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("richiesta_adesione", sa.Date(), nullable=True))
    op.add_column("items", sa.Column("ticket_cart", sa.Text(), nullable=True))
    op.add_column("items", sa.Column("referente_adesione", sa.Text(), nullable=True))
    op.add_column("items", sa.Column("referente_tecnico_applicativo", sa.Text(), nullable=True))
    op.add_column("items", sa.Column("test_case_1", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("test_case_2", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("test_case_3", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("test_case_4", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("data_richiesta_certificato", sa.Date(), nullable=True))
    op.add_column("items", sa.Column("data_emissione_certificato", sa.Date(), nullable=True))
    op.add_column("items", sa.Column("estar_autorizzazione_prod", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("data_invio_certificati_ente_adesione", sa.Date(), nullable=True))
    op.add_column("items", sa.Column("data_accreditamento", sa.Date(), nullable=True))
    op.add_column("items", sa.Column("data_autorizzazione_rt_passaggio_in_produzione", sa.Date(), nullable=True))
    op.add_column("items", sa.Column("psw_certificato_raki", sa.Text(), nullable=True))

def downgrade() -> None:
    cols = ["psw_certificato_raki","data_autorizzazione_rt_passaggio_in_produzione","data_accreditamento",
            "data_invio_certificati_ente_adesione","estar_autorizzazione_prod","data_emissione_certificato",
            "data_richiesta_certificato","test_case_4","test_case_3","test_case_2","test_case_1",
            "referente_tecnico_applicativo","referente_adesione","ticket_cart","richiesta_adesione",
            "software_version_check","software_name_check","fornitore_name_check",
            "codice_regione_accreditamento","asl_convenzionato","accreditamento","convenzionato",
            "software_docu_profile","software_version","software_name","fornitore_name","p_iva","structure_code","structure_name"]
    for c in cols:
        op.drop_column("items", c)
    op.add_column("items", sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False))
    op.add_column("items", sa.Column("name", sa.Text(), nullable=False))
