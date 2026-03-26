"""update items schema to new anagrafica structure

Revision ID: 20251118_0003
Revises: 20251028_0002
Create Date: 2025-11-18 00:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251118_0003"
down_revision = "20251028_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # Campi ANAGRAFICA - tutti nuovi, NOT NULL
    # Per evitare problemi con righe esistenti, usiamo un server_default
    # temporaneo e poi lo rimuoviamo.
    # ------------------------------------------------------------------
    op.add_column(
        "items",
        sa.Column(
            "Rappresentante_nomeRapp",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Rappresentante_cognomeRapp",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Rappresentante_PEC",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )

    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_denominazione",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_partitaIva",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_tipoSoggetto",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_provincia",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_comune",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_indirizzo",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_cap",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_telefonoRapp",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_email",
            sa.String(),
            nullable=False,
            server_default="",
        ),
    )

    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_accreditamento",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_convenzioneSSR",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_convenzioneASL",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "Anagrafica_numeroSedi",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # ------------------------------------------------------------------
    # Campi LDO
    # ------------------------------------------------------------------
    op.add_column("items", sa.Column("LDO_LDO", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("LDO_LDOdigitale", sa.Boolean(), nullable=True))
    op.add_column(
        "items",
        sa.Column("LDO_LDOdigitale_TDTLDO", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("LDO_LDOdigitale_applicativoLDO", sa.String(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column(
            "LDO_LDOdigitale_fornitoreApplicativoLDO",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "LDO_LDOdigitale_versioneApplicativoLDO",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column("LDO_LDOdigitale_PDFfirmatiLDO", sa.Boolean(), nullable=True),
    )

    # ------------------------------------------------------------------
    # Campi LAB
    # ------------------------------------------------------------------
    op.add_column("items", sa.Column("LAB_LAB", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("LAB_LABdigitale", sa.Boolean(), nullable=True))
    op.add_column(
        "items",
        sa.Column("LAB_LABdigitale_TDTLAB", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("LAB_LABdigitale_applicativoLAB", sa.String(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column(
            "LAB_LABdigitale_fornitoreApplicativoLAB",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "LAB_LABdigitale_versioneApplicativoLAB",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column("LAB_LABdigitale_PDFfirmatiLAB", sa.Boolean(), nullable=True),
    )

    # ------------------------------------------------------------------
    # Campi RAD
    # ------------------------------------------------------------------
    op.add_column("items", sa.Column("RAD_RAD", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("RAD_RADdigitale", sa.Boolean(), nullable=True))
    op.add_column(
        "items",
        sa.Column("RAD_RADdigitale_TDTRAD", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RAD_RADdigitale_applicativoRAD", sa.String(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column(
            "RAD_RADdigitale_fornitoreApplicativoRAD",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "RAD_RADdigitale_versioneApplicativoRAD",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column("RAD_RADdigitale_PDFfirmatiRAD", sa.Boolean(), nullable=True),
    )

    # ------------------------------------------------------------------
    # Campi RSA
    # ------------------------------------------------------------------
    op.add_column("items", sa.Column("RSA_RSA", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("RSA_RSAdigitale", sa.Boolean(), nullable=True))
    op.add_column(
        "items",
        sa.Column("RSA_RSAdigitale_TDTRSA", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RSA_RSAdigitale_applicativoRSA", sa.String(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column(
            "RSA_RSAdigitale_fornitoreApplicativoRSA",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "RSA_RSAdigitale_versioneApplicativoRSA",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column("RSA_RSAdigitale_PDFfirmatiRSA", sa.Boolean(), nullable=True),
    )

    # ------------------------------------------------------------------
    # Campi RAP
    # ------------------------------------------------------------------
    op.add_column("items", sa.Column("RAP_RAP", sa.Boolean(), nullable=True))
    op.add_column("items", sa.Column("RAP_RAPdigitale", sa.Boolean(), nullable=True))
    op.add_column(
        "items",
        sa.Column("RAP_RAPdigitale_TDTRAP", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RAP_RAPdigitale_applicativoRAP", sa.String(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column(
            "RAP_RAPdigitale_fornitoreApplicativoRAP",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "RAP_RAPdigitale_versioneApplicativoRAP",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column("RAP_RAPdigitale_PDFfirmatiRAP", sa.Boolean(), nullable=True),
    )

    # ------------------------------------------------------------------
    # Altre informazioni
    # ------------------------------------------------------------------
    op.add_column(
        "items",
        sa.Column(
            "AltreInformazioni_ambitiPrestazioni_0",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "AltreInformazioni_ambitiPrestazioni_1",
            sa.String(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "AltreInformazioni_finanziamentoPNRR",
            sa.Boolean(),
            nullable=True,
        ),
    )
    op.add_column(
        "items",
        sa.Column(
            "AltreInformazioni_conservazioneDigitale",
            sa.Boolean(),
            nullable=True,
        ),
    )

    # ------------------------------------------------------------------
    # Check LDO/LAB/RAD/RSA/RPA (nuovi, ATTENZIONE: NON i vecchi)
    # ------------------------------------------------------------------
    op.add_column(
        "items",
        sa.Column("LDO_fornitore_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("LDO_software_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("LDO_software_version_check", sa.Boolean(), nullable=True),
    )

    op.add_column(
        "items",
        sa.Column("LAB_fornitore_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("LAB_software_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("LAB_software_version_check", sa.Boolean(), nullable=True),
    )

    op.add_column(
        "items",
        sa.Column("RAD_fornitore_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RAD_software_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RAD_software_version_check", sa.Boolean(), nullable=True),
    )

    op.add_column(
        "items",
        sa.Column("RSA_fornitore_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RSA_software_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RSA_software_version_check", sa.Boolean(), nullable=True),
    )

    op.add_column(
        "items",
        sa.Column("RPA_fornitore_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RPA_software_name_check", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "items",
        sa.Column("RPA_software_version_check", sa.Boolean(), nullable=True),
    )

    # ------------------------------------------------------------------
    # Certificato
    # ------------------------------------------------------------------
    op.add_column(
        "items",
        sa.Column("CN_Certificato", sa.String(), nullable=True),
    )

    # ------------------------------------------------------------------
    # Rimuovo i server_default provvisori sui campi NOT NULL anagrafici
    # ------------------------------------------------------------------
    for col in [
        "Rappresentante_nomeRapp",
        "Rappresentante_cognomeRapp",
        "Rappresentante_PEC",
        "Anagrafica_denominazione",
        "Anagrafica_partitaIva",
        "Anagrafica_tipoSoggetto",
        "Anagrafica_provincia",
        "Anagrafica_comune",
        "Anagrafica_indirizzo",
        "Anagrafica_cap",
        "Anagrafica_telefonoRapp",
        "Anagrafica_email",
        "Anagrafica_accreditamento",
        "Anagrafica_convenzioneSSR",
        "Anagrafica_convenzioneASL",
        "Anagrafica_numeroSedi",
    ]:
        op.alter_column("items", col, server_default=None)


def downgrade() -> None:
    # Downgrade: rimuovo le colonne aggiunte in upgrade (ordine inverso)

    # Certificato
    op.drop_column("items", "CN_Certificato")

    # Check LDO/LAB/RAD/RSA/RPA
    op.drop_column("items", "RPA_software_version_check")
    op.drop_column("items", "RPA_software_name_check")
    op.drop_column("items", "RPA_fornitore_name_check")

    op.drop_column("items", "RSA_software_version_check")
    op.drop_column("items", "RSA_software_name_check")
    op.drop_column("items", "RSA_fornitore_name_check")

    op.drop_column("items", "RAD_software_version_check")
    op.drop_column("items", "RAD_software_name_check")
    op.drop_column("items", "RAD_fornitore_name_check")

    op.drop_column("items", "LAB_software_version_check")
    op.drop_column("items", "LAB_software_name_check")
    op.drop_column("items", "LAB_fornitore_name_check")

    op.drop_column("items", "LDO_software_version_check")
    op.drop_column("items", "LDO_software_name_check")
    op.drop_column("items", "LDO_fornitore_name_check")

    # Altre informazioni
    op.drop_column("items", "AltreInformazioni_conservazioneDigitale")
    op.drop_column("items", "AltreInformazioni_finanziamentoPNRR")
    op.drop_column("items", "AltreInformazioni_ambitiPrestazioni_1")
    op.drop_column("items", "AltreInformazioni_ambitiPrestazioni_0")

    # RAP
    op.drop_column("items", "RAP_RAPdigitale_PDFfirmatiRAP")
    op.drop_column("items", "RAP_RAPdigitale_versioneApplicativoRAP")
    op.drop_column("items", "RAP_RAPdigitale_fornitoreApplicativoRAP")
    op.drop_column("items", "RAP_RAPdigitale_applicativoRAP")
    op.drop_column("items", "RAP_RAPdigitale_TDTRAP")
    op.drop_column("items", "RAP_RAPdigitale")
    op.drop_column("items", "RAP_RAP")

    # RSA
    op.drop_column("items", "RSA_RSAdigitale_PDFfirmatiRSA")
    op.drop_column("items", "RSA_RSAdigitale_versioneApplicativoRSA")
    op.drop_column("items", "RSA_RSAdigitale_fornitoreApplicativoRSA")
    op.drop_column("items", "RSA_RSAdigitale_applicativoRSA")
    op.drop_column("items", "RSA_RSAdigitale_TDTRSA")
    op.drop_column("items", "RSA_RSAdigitale")
    op.drop_column("items", "RSA_RSA")

    # RAD
    op.drop_column("items", "RAD_RADdigitale_PDFfirmatiRAD")
    op.drop_column("items", "RAD_RADdigitale_versioneApplicativoRAD")
    op.drop_column("items", "RAD_RADdigitale_fornitoreApplicativoRAD")
    op.drop_column("items", "RAD_RADdigitale_applicativoRAD")
    op.drop_column("items", "RAD_RADdigitale_TDTRAD")
    op.drop_column("items", "RAD_RADdigitale")
    op.drop_column("items", "RAD_RAD")

    # LAB
    op.drop_column("items", "LAB_LABdigitale_PDFfirmatiLAB")
    op.drop_column("items", "LAB_LABdigitale_versioneApplicativoLAB")
    op.drop_column("items", "LAB_LABdigitale_fornitoreApplicativoLAB")
    op.drop_column("items", "LAB_LABdigitale_applicativoLAB")
    op.drop_column("items", "LAB_LABdigitale_TDTLAB")
    op.drop_column("items", "LAB_LABdigitale")
    op.drop_column("items", "LAB_LAB")

    # LDO
    op.drop_column("items", "LDO_LDOdigitale_PDFfirmatiLDO")
    op.drop_column("items", "LDO_LDOdigitale_versioneApplicativoLDO")
    op.drop_column("items", "LDO_LDOdigitale_fornitoreApplicativoLDO")
    op.drop_column("items", "LDO_LDOdigitale_applicativoLDO")
    op.drop_column("items", "LDO_LDOdigitale_TDTLDO")
    op.drop_column("items", "LDO_LDOdigitale")
    op.drop_column("items", "LDO_LDO")

    # Anagrafica
    op.drop_column("items", "Anagrafica_numeroSedi")
    op.drop_column("items", "Anagrafica_convenzioneASL")
    op.drop_column("items", "Anagrafica_convenzioneSSR")
    op.drop_column("items", "Anagrafica_accreditamento")
    op.drop_column("items", "Anagrafica_email")
    op.drop_column("items", "Anagrafica_telefonoRapp")
    op.drop_column("items", "Anagrafica_cap")
    op.drop_column("items", "Anagrafica_indirizzo")
    op.drop_column("items", "Anagrafica_comune")
    op.drop_column("items", "Anagrafica_provincia")
    op.drop_column("items", "Anagrafica_tipoSoggetto")
    op.drop_column("items", "Anagrafica_partitaIva")
    op.drop_column("items", "Anagrafica_denominazione")
    op.drop_column("items", "Rappresentante_PEC")
    op.drop_column("items", "Rappresentante_cognomeRapp")
    op.drop_column("items", "Rappresentante_nomeRapp")
