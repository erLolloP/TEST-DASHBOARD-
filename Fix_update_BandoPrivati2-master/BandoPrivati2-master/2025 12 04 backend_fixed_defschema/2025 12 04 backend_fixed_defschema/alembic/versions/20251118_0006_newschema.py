from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251118_0006"
down_revision = "20251118_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- RPA -> RAP: rename colonne di check ---
    op.alter_column("items", "RPA_fornitore_name_check",
                    new_column_name="RAP_fornitore_name_check")
    op.alter_column("items", "RPA_software_name_check",
                    new_column_name="RAP_software_name_check")
    op.alter_column("items", "RPA_software_version_check",
                    new_column_name="RAP_software_version_check")

    # --- Drop check globali ---
    op.drop_column("items", "fornitore_name_check")
    op.drop_column("items", "software_name_check")
    op.drop_column("items", "software_version_check")

    # --- RPA -> RAP: rename colonne certificato ---
    op.alter_column("items", "RPA_CN_Certificato",
                    new_column_name="RAP_CN_Certificato")
    op.alter_column("items", "RPA_richiesta_adesione",
                    new_column_name="RAP_richiesta_adesione")
    op.alter_column("items", "RPA_ticket_cart",
                    new_column_name="RAP_ticket_cart")
    op.alter_column("items", "RPA_referente_adesione",
                    new_column_name="RAP_referente_adesione")
    op.alter_column("items", "RPA_referente_tecnico_applicativo",
                    new_column_name="RAP_referente_tecnico_applicativo")
    op.alter_column("items", "RPA_test_validate_create",
                    new_column_name="RAP_test_validate_create")
    op.alter_column("items", "RPA_test_sostituzione",
                    new_column_name="RAP_test_sostituzione")
    op.alter_column("items", "RPA_test_aggiornamento",
                    new_column_name="RAP_test_aggiornamento")
    op.alter_column("items", "RPA_test_eliminazione",
                    new_column_name="RAP_test_eliminazione")
    op.alter_column("items", "RPA_data_richiesta_certificato",
                    new_column_name="RAP_data_richiesta_certificato")
    op.alter_column("items", "RPA_data_emissione_certificato",
                    new_column_name="RAP_data_emissione_certificato")
    op.alter_column("items", "RPA_autorizzazione_prod",
                    new_column_name="RAP_autorizzazione_prod")
    op.alter_column("items", "RPA_data_invio_certificati_ente_adesione",
                    new_column_name="RAP_data_invio_certificati_ente_adesione")
    op.alter_column("items", "RPA_data_accreditamento",
                    new_column_name="RAP_data_accreditamento")
    op.alter_column("items", "RPA_data_autorizzazione_prod",
                    new_column_name="RAP_data_autorizzazione_prod")
    op.alter_column("items", "RPA_psw_certificato_raki",
                    new_column_name="RAP_psw_certificato_raki")


def downgrade() -> None:
    # --- RAP -> RPA: rinomina indietro le colonne certificato ---
    op.alter_column("items", "RAP_psw_certificato_raki",
                    new_column_name="RPA_psw_certificato_raki")
    op.alter_column("items", "RAP_data_autorizzazione_prod",
                    new_column_name="RPA_data_autorizzazione_prod")
    op.alter_column("items", "RAP_data_accreditamento",
                    new_column_name="RPA_data_accreditamento")
    op.alter_column("items", "RAP_data_invio_certificati_ente_adesione",
                    new_column_name="RPA_data_invio_certificati_ente_adesione")
    op.alter_column("items", "RAP_autorizzazione_prod",
                    new_column_name="RPA_autorizzazione_prod")
    op.alter_column("items", "RAP_data_emissione_certificato",
                    new_column_name="RPA_data_emissione_certificato")
    op.alter_column("items", "RAP_data_richiesta_certificato",
                    new_column_name="RPA_data_richiesta_certificato")
    op.alter_column("items", "RAP_test_eliminazione",
                    new_column_name="RPA_test_eliminazione")
    op.alter_column("items", "RAP_test_aggiornamento",
                    new_column_name="RPA_test_aggiornamento")
    op.alter_column("items", "RAP_test_sostituzione",
                    new_column_name="RPA_test_sostituzione")
    op.alter_column("items", "RAP_test_validate_create",
                    new_column_name="RPA_test_validate_create")
    op.alter_column("items", "RAP_referente_tecnico_applicativo",
                    new_column_name="RPA_referente_tecnico_applicativo")
    op.alter_column("items", "RAP_referente_adesione",
                    new_column_name="RPA_referente_adesione")
    op.alter_column("items", "RAP_ticket_cart",
                    new_column_name="RPA_ticket_cart")
    op.alter_column("items", "RAP_richiesta_adesione",
                    new_column_name="RPA_richiesta_adesione")
    op.alter_column("items", "RAP_CN_Certificato",
                    new_column_name="RPA_CN_Certificato")

    # --- Riaggiungo i check globali (tutti nullable=True) ---
    op.add_column(
        "items",
        sa.Column("fornitore_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("software_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("software_version_check", sa.Boolean(), nullable=True),
    )

    # --- RAP -> RPA: rinomina indietro le colonne di check ---
    op.alter_column("items", "RAP_fornitore_name_check",
                    new_column_name="RPA_fornitore_name_check")
    op.alter_column("items", "RAP_software_name_check",
                    new_column_name="RPA_software_name_check")
    op.alter_column("items", "RAP_software_version_check",
                    new_column_name="RPA_software_version_check")
