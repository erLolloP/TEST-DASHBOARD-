from fastapi import (
    APIRouter,
    Depends,
    Query,
    HTTPException,
    UploadFile,
    File,
)
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from datetime import datetime, date, timezone
import csv
import io
import json
import ast
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.core.auth import require_levels
from app.db.session import get_session
from app.db.models import Item
from app.schemas.data import DashboardStatsOut, ItemCreate, ItemOut, ItemUpdate

router = APIRouter(prefix="/data", tags=["data"])


CSV_TO_DB_COLUMN_MAP = {
    "dati_containerRappresentante_nomeRapp": "Rappresentante_nomeRapp",
    "dati_containerRappresentante_cognomeRapp": "Rappresentante_cognomeRapp",
    "dati_containerRappresentante_PEC": "Rappresentante_PEC",
    "dati_containerAnagrafica_denominazione": "Anagrafica_denominazione",
    "dati_containerAnagrafica_partitaIva": "Anagrafica_partitaIva",
    "dati_containerAnagrafica_tipoSoggetto": "Anagrafica_tipoSoggetto",
    "dati_containerAnagrafica_provincia": "Anagrafica_provincia",
    "dati_containerAnagrafica_comune": "Anagrafica_comune",
    "dati_containerAnagrafica_indirizzo": "Anagrafica_indirizzo",
    "dati_containerAnagrafica_cap": "Anagrafica_cap",
    "dati_containerAnagrafica_telefonoRapp": "Anagrafica_telefonoRapp",
    "dati_containerAnagrafica_email": "Anagrafica_email",
    "dati_containerAnagrafica_accreditamento": "Anagrafica_accreditamento",
    "dati_containerAnagrafica_convenzioneSSR": "Anagrafica_convenzioneSSR",
    "dati_containerAnagrafica_convenzioneASL": "Anagrafica_convenzioneASL",
    "dati_containerAnagrafica_numeroSedi": "Anagrafica_numeroSedi",
    "dati_containerAnagrafica_numeroDiSediDiStrutturePerPIva": "Anagrafica_numeroSedi",
    "dati_containerAltreInformazioni_ambitiPrestazioni_0": "AltreInformazioni_ambitiPrestazioni_0",
    "dati_containerAltreInformazioni_ambitiPrestazioni_1": "AltreInformazioni_ambitiPrestazioni_1",
    "dati_containerAltreInformazioni_finanziamentoPNRR": "AltreInformazioni_finanziamentoPNRR",
    "dati_containerAltreInformazioni_conservazioneDigitale": "AltreInformazioni_conservazioneDigitale",
    "dati_containerLDO_LDO": "LDO_LDO",
    "dati_containerLDO_LDOdigitale": "LDO_LDOdigitale",
    "dati_containerLDO_containerLDOdigitale_TDTLDO": "LDO_LDOdigitale_TDTLDO",
    "dati_containerLDO_containerLDOdigitale_applicativoLDO": "LDO_LDOdigitale_applicativoLDO",
    "dati_containerLDO_containerLDOdigitale_fornitoreApplicativoLDO": "LDO_LDOdigitale_fornitoreApplicativoLDO",
    "dati_containerLDO_containerLDOdigitale_versioneApplicativoLDO": "LDO_LDOdigitale_versioneApplicativoLDO",
    "dati_containerLDO_containerLDOdigitale_PDFfirmatiLDO": "LDO_LDOdigitale_PDFfirmatiLDO",
    "dati_containerLAB_LAB": "LAB_LAB",
    "dati_containerLAB_LABdigitale": "LAB_LABdigitale",
    "dati_containerLAB_containerLABdigitale_TDTLAB": "LAB_LABdigitale_TDTLAB",
    "dati_containerLAB_containerLABdigitale_applicativoLAB": "LAB_LABdigitale_applicativoLAB",
    "dati_containerLAB_containerLABdigitale_fornitoreApplicativoLAB": "LAB_LABdigitale_fornitoreApplicativoLAB",
    "dati_containerLAB_containerLABdigitale_versioneApplicativoLAB": "LAB_LABdigitale_versioneApplicativoLAB",
    "dati_containerLAB_containerLABdigitale_PDFfirmatiLAB": "LAB_LABdigitale_PDFfirmatiLAB",
    "dati_containerRAD_RAD": "RAD_RAD",
    "dati_containerRAD_RADdigitale": "RAD_RADdigitale",
    "dati_containerRAD_containerRADdigitale_TDTRAD": "RAD_RADdigitale_TDTRAD",
    "dati_containerRAD_containerRADdigitale_applicativoRAD": "RAD_RADdigitale_applicativoRAD",
    "dati_containerRAD_containerRADdigitale_fornitoreApplicativoRAD": "RAD_RADdigitale_fornitoreApplicativoRAD",
    "dati_containerRAD_containerRADdigitale_versioneApplicativoRAD": "RAD_RADdigitale_versioneApplicativoRAD",
    "dati_containerRAD_containerRADdigitale_PDFfirmatiRAD": "RAD_RADdigitale_PDFfirmatiRAD",
    "dati_containerRSA_RSA": "RSA_RSA",
    "dati_containerRSA_RSAdigitale": "RSA_RSAdigitale",
    "dati_containerRSA_containerRSAdigitale_TDTRSA": "RSA_RSAdigitale_TDTRSA",
    "dati_containerRSA_containerRSAdigitale_applicativoRSA": "RSA_RSAdigitale_applicativoRSA",
    "dati_containerRSA_containerRSAdigitale_fornitoreApplicativoRSA": "RSA_RSAdigitale_fornitoreApplicativoRSA",
    "dati_containerRSA_containerRSAdigitale_versioneApplicativoRSA": "RSA_RSAdigitale_versioneApplicativoRSA",
    "dati_containerRSA_containerRSAdigitale_PDFfirmatiRSA": "RSA_RSAdigitale_PDFfirmatiRSA",
    "dati_containerRAP_RAP": "RAP_RAP",
    "dati_containerRAP_RAPdigitale": "RAP_RAPdigitale",
    "dati_containerRAP_containerRAPdigitale_TDTRAP": "RAP_RAPdigitale_TDTRAP",
    "dati_containerRAP_containerRAPdigitale_applicativoRAP": "RAP_RAPdigitale_applicativoRAP",
    "dati_containerRAP_containerRAPdigitale_fornitoreApplicativoRAP": "RAP_RAPdigitale_fornitoreApplicativoRAP",
    "dati_containerRAP_containerRAPdigitale_versioneApplicativoRAP": "RAP_RAPdigitale_versioneApplicativoRAP",
    "dati_containerRAP_containerRAPdigitale_PDFfirmatiRAP": "RAP_RAPdigitale_PDFfirmatiRAP",
}

DB_TO_CSV_COLUMN_MAP = {db_col: csv_col for csv_col, db_col in CSV_TO_DB_COLUMN_MAP.items()}


def _parse_integer_loose(value: str) -> int:
    normalized = value.replace(",", ".")
    numeric_value = float(normalized)
    if numeric_value.is_integer():
        return int(numeric_value)
    return int(numeric_value)


def _parse_boolean_loose(value: str) -> bool:
    normalized = value.strip().lower()

    # Gestione casi comuni di mojibake (es. "S√¨" invece di "Sì").
    normalized = normalized.replace("√¨", "ì")

    # Considera solo il primo token per supportare frasi come
    # "Sì, utilizza un repository interno".
    first_token = normalized
    for separator in (",", ";", ":", "(", ")", "-", "\n", "\t"):
        first_token = first_token.split(separator, 1)[0].strip()

    if first_token in {"true", "1", "yes", "y", "si", "sì", "s"}:
        return True
    if first_token in {"false", "0", "no", "n", "non"}:
        return False

    if first_token.startswith(("si", "sì", "yes", "true")):
        return True
    if first_token.startswith(("no", "non", "false")):
        return False

    raise ValueError(f"Valore booleano non valido '{value}'")


def _parse_csv_value(value: str, col_type: sa.types.TypeEngine):
    try:
        is_bool_col = getattr(col_type, "python_type", None) is bool
    except Exception:
        is_bool_col = False

    if is_bool_col:
        return _parse_boolean_loose(value)

    if isinstance(col_type, sa.Date):
        return date.fromisoformat(value)

    if isinstance(col_type, postgresql.JSONB):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return ast.literal_eval(value)

    if isinstance(col_type, sa.Integer):
        return _parse_integer_loose(value)

    return value


async def _get_or_404(session: AsyncSession, item_id: UUID) -> Item:
    res = await session.execute(select(Item).where(Item.id == item_id))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")
    return obj


async def _get_by_partita_iva_or_404(
    session: AsyncSession, partita_iva: str
) -> Item:
    res = await session.execute(
        select(Item)
        .where(Item.Anagrafica_partitaIva == partita_iva)
        .order_by(Item.created_at.asc(), Item.id.asc())
    )
    obj = res.scalars().first()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=(
                "Nessun elemento trovato nel database con "
                f"Anagrafica_partitaIva = '{partita_iva}'."
            ),
        )
    return obj


# -------------------------------------------------------------------------
# CREATE (admin)
# -------------------------------------------------------------------------
@router.post(
    "",
    response_model=ItemOut,
    status_code=201,
    dependencies=[Depends(require_levels("admin"))],
)
async def create_item(
    body: ItemCreate, session: AsyncSession = Depends(get_session)
):
    item = Item(
        # Anagrafica Rappresentante
        Rappresentante_nomeRapp=body.Rappresentante_nomeRapp,
        Rappresentante_cognomeRapp=body.Rappresentante_cognomeRapp,
        Rappresentante_PEC=body.Rappresentante_PEC,
        # Anagrafica Struttura
        Anagrafica_denominazione=body.Anagrafica_denominazione,
        Anagrafica_partitaIva=body.Anagrafica_partitaIva,
        Anagrafica_tipoSoggetto=body.Anagrafica_tipoSoggetto,
        Anagrafica_provincia=body.Anagrafica_provincia,
        Anagrafica_comune=body.Anagrafica_comune,
        Anagrafica_indirizzo=body.Anagrafica_indirizzo,
        Anagrafica_cap=body.Anagrafica_cap,
        Anagrafica_telefonoRapp=body.Anagrafica_telefonoRapp,
        Anagrafica_email=body.Anagrafica_email,
        Anagrafica_accreditamento=body.Anagrafica_accreditamento,
        Anagrafica_convenzioneSSR=body.Anagrafica_convenzioneSSR,
        Anagrafica_convenzioneASL=body.Anagrafica_convenzioneASL,
        Anagrafica_numeroSedi=body.Anagrafica_numeroSedi,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


# -------------------------------------------------------------------------
# LIST (reader/editor/admin)
# -------------------------------------------------------------------------
@router.get(
    "",
    response_model=list[ItemOut],
    dependencies=[Depends(require_levels("reader", "editor", "admin"))],
)
async def list_items(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    stmt = select(Item).order_by(Item.created_at.desc())
    rows = (await session.execute(stmt.limit(limit).offset(offset))).scalars().all()
    return rows




@router.get(
    "/dashboard",
    response_model=DashboardStatsOut,
    dependencies=[Depends(require_levels("reader", "editor", "admin"))],
)
async def get_dashboard_stats(session: AsyncSession = Depends(get_session)):
    totale_fondi = 500_000
    contributo_per_struttura = 10_000

    total_strutture = await session.scalar(select(func.count(Item.id)))
    total_strutture = int(total_strutture or 0)

    supplier_columns = {
        "LDO": Item.LDO_LDOdigitale_fornitoreApplicativoLDO,
        "LAB": Item.LAB_LABdigitale_fornitoreApplicativoLAB,
        "RAD": Item.RAD_RADdigitale_fornitoreApplicativoRAD,
        "RSA": Item.RSA_RSAdigitale_fornitoreApplicativoRSA,
        "RAP": Item.RAP_RAPdigitale_fornitoreApplicativoRAP,
    }

    fornitori_unici_per_tipologia: dict[str, int] = {}
    for tipologia, column in supplier_columns.items():
        count_unique = await session.scalar(
            select(func.count(func.distinct(column))).where(
                column.is_not(None),
                column != "",
            )
        )
        fornitori_unici_per_tipologia[tipologia] = int(count_unique or 0)

    costo_totale_strutture = total_strutture * contributo_per_struttura
    residuo_fondi = totale_fondi - costo_totale_strutture

    return DashboardStatsOut(
        total_strutture=total_strutture,
        fornitori_unici_per_tipologia=fornitori_unici_per_tipologia,
        totale_fondi=totale_fondi,
        residuo_fondi=residuo_fondi,
        costo_totale_strutture=costo_totale_strutture,
    )


# -------------------------------------------------------------------------
# EXPORT to CSV (reader/editor/admin)
# -------------------------------------------------------------------------
@router.get(
    "/export-csv",
    dependencies=[Depends(require_levels("reader", "editor", "admin"))],
)
async def export_items_to_csv(
    session: AsyncSession = Depends(get_session),
):
    stmt = select(Item).order_by(Item.created_at.desc())
    rows = (await session.execute(stmt)).scalars().all()

    # Preparo CSV in memoria
    output = io.StringIO()
    writer = csv.writer(output)

    # Tutte le colonne del modello Item, in ordine
    columns = [col.name for col in Item.__table__.columns]
    csv_columns = [DB_TO_CSV_COLUMN_MAP.get(col, col) for col in columns]

    # Header
    writer.writerow(csv_columns)

    # Righe
    for item in rows:
        writer.writerow([getattr(item, col) for col in columns])

    output.seek(0)
    csv_data = output.getvalue()

    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="items_export.csv"'
        },
    )


# -------------------------------------------------------------------------
# IMPORT from CSV (admin)
# -------------------------------------------------------------------------
@router.post(
    "/import-csv",
    response_model=list[ItemOut],
    status_code=201,
    dependencies=[Depends(require_levels("admin"))],
)
async def import_items_from_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    # Controllo estensione
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Il file deve essere un CSV (estensione .csv).",
        )

    # Leggo il contenuto del file
    raw_bytes = await file.read()
    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Impossibile decodificare il file CSV: assicurati che sia in UTF-8.",
        )

    csv_file = io.StringIO(text)
    reader = csv.DictReader(csv_file)

    # 1) Controllo header
    if not reader.fieldnames:
        raise HTTPException(
            status_code=400,
            detail=(
                "CSV senza intestazione: la prima riga deve contenere i "
                "nomi delle colonne."
            ),
        )

    csv_headers = set(reader.fieldnames)

    table = Item.__table__

    # Nel nuovo CSV possono esserci molte colonne non persistite nel DB: le ignoriamo.

    # Campi obbligatori: tutte le colonne DB non nullable (esclusi PK e timestamp).
    required_db_columns = {
        col.name
        for col in table.columns
        if (
            not col.nullable
            and not col.primary_key
            and col.name not in {"created_at", "updated_at"}
        )
    }

    required_csv_columns = {
        DB_TO_CSV_COLUMN_MAP.get(col_name, col_name)
        for col_name in required_db_columns
    }

    missing_required_in_header = required_csv_columns - csv_headers
    if missing_required_in_header:
        raise HTTPException(
            status_code=400,
            detail=(
                "Il CSV deve contenere queste colonne obbligatorie: "
                f"{', '.join(sorted(missing_required_in_header))}."
            ),
        )

    # Colonne inseribili
    insertable_columns = {
        col.name
        for col in table.columns
        if not col.primary_key and col.name not in {"created_at", "updated_at"}
    }

    column_map = {col.name: col for col in table.columns}

    # Qui salvo i dati "grezzi" per ogni riga valida del CSV
    rows_data: list[dict[str, object]] = []

    # 2) Leggo il CSV e costruisco i dict (NON ancora Item)
    for row in reader:
        data: dict[str, object] = {}

        for csv_key, value in row.items():
            key = CSV_TO_DB_COLUMN_MAP.get(csv_key, csv_key)
            if key not in insertable_columns:
                continue

            if value is None:
                python_value = None
            else:
                value = value.strip()
                if value == "":
                    python_value = None
                else:
                    col = column_map[key]
                    col_type = col.type

                    try:
                        python_value = _parse_csv_value(value, col_type)
                    except Exception as e:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                f"Valore non valido per la colonna '{key}' "
                                f"alla riga {reader.line_num}: {e}"
                            ),
                        )

            data[key] = python_value

        # Se riga completamente vuota → skip
        if not any(v is not None for v in data.values()):
            continue

        # Controllo campi obbligatori (non nulli) su tutte le colonne DB non nullable.
        for col_name in required_db_columns:
            if data.get(col_name) is None:
                csv_col_name = DB_TO_CSV_COLUMN_MAP.get(col_name, col_name)
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Campo obbligatorio '{csv_col_name}' mancante o vuoto "
                        f"alla riga {reader.line_num}."
                    ),
                )

        rows_data.append(data)

    if not rows_data:
        raise HTTPException(
            status_code=400,
            detail="Il CSV non contiene righe valide da inserire.",
        )

    # 3) Controllo delle partite IVA contro il DB
    csv_piva_set: set[str] = set()
    for data in rows_data:
        piva = (data.get("Anagrafica_partitaIva") or "").strip()
        if piva:
            csv_piva_set.add(piva)

    existing_piva_set: set[str] = set()
    if csv_piva_set:
        result = await session.execute(
            select(Item.Anagrafica_partitaIva).where(
                Item.Anagrafica_partitaIva.in_(csv_piva_set)
            )
        )
        existing_piva_set = {
            row[0] for row in result.fetchall() if row[0] is not None
        }

    # 4) Creo gli Item SOLO per le partite IVA NON presenti nel DB
    items_to_add: list[Item] = []
    for data in rows_data:
        piva = (data.get("Anagrafica_partitaIva") or "").strip()
        # se per qualche motivo è vuota qui, il required l'ha già bloccata prima
        if piva and piva in existing_piva_set:
            # già presente nel DB → salta
            continue
        items_to_add.append(Item(**data))

    if not items_to_add:
        raise HTTPException(
            status_code=400,
            detail=(
                "Nessuna riga inserita: tutte le Anagrafica_partitaIva presenti "
                "nel CSV risultano già presenti nel database."
            ),
        )

    # 5) Inserimento effettivo
    session.add_all(items_to_add)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Errore di integrità durante l'inserimento dei dati: {str(e.orig)}",
        )

    for item in items_to_add:
        await session.refresh(item)

    return items_to_add




# -------------------------------------------------------------------------
# UPDATE from CSV by Anagrafica_partitaIva (admin)
# -------------------------------------------------------------------------
@router.post(
    "/update-from-csv",
    response_model=list[ItemOut],
    dependencies=[Depends(require_levels("admin"))],
)
async def update_items_from_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Il file deve essere un CSV (estensione .csv).",
        )

    raw_bytes = await file.read()
    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Impossibile decodificare il file CSV: assicurati che sia in UTF-8.",
        )

    csv_file = io.StringIO(text)
    reader = csv.DictReader(csv_file)

    if not reader.fieldnames:
        raise HTTPException(
            status_code=400,
            detail=(
                "CSV senza intestazione: la prima riga deve contenere i "
                "nomi delle colonne."
            ),
        )

    csv_headers = set(reader.fieldnames)

    # campo usato come chiave di match
    match_field = "dati_containerAnagrafica_partitaIva"

    if match_field not in csv_headers:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Il CSV deve contenere la colonna '{match_field}' "
                "per poter effettuare l'aggiornamento."
            ),
        )

    table = Item.__table__

    updatable_columns = {
        col.name
        for col in table.columns
        if not col.primary_key and col.name not in {"created_at", "updated_at"}
    }

    required_insert_columns = {
        col.name
        for col in table.columns
        if (
            not col.primary_key
            and col.name not in {"created_at", "updated_at"}
            and not col.nullable
            and col.server_default is None
            and col.default is None
        )
    }

    column_map = {col.name: col for col in table.columns}

    csv_rows: list[dict] = []
    match_values: set[str] = set()

    for row in reader:
        line_num = reader.line_num

        raw_match = (row.get(match_field) or "").strip()
        if not raw_match:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Riga senza {match_field} alla riga "
                    f"{line_num}: il campo è obbligatorio per l'aggiornamento."
                ),
            )

        match_values.add(raw_match)

        data: dict[str, object] = {}

        for csv_key, value in row.items():
            key = CSV_TO_DB_COLUMN_MAP.get(csv_key, csv_key)
            if key not in updatable_columns:
                continue

            if value is None:
                python_value = None
            else:
                value = value.strip()
                if value == "":
                    python_value = None
                else:
                    col = column_map[key]
                    col_type = col.type

                    try:
                        python_value = _parse_csv_value(value, col_type)
                    except Exception as e:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                f"Valore non valido per la colonna '{key}' "
                                f"alla riga {line_num}: {e}"
                            ),
                        )

            data[key] = python_value

        csv_rows.append(
            {
                "match": raw_match,
                "data": data,
                "line_num": line_num,
            }
        )

    if not csv_rows:
        raise HTTPException(
            status_code=400,
            detail="Il CSV non contiene righe valide da elaborare.",
        )

    # Recupero tutte le righe del DB con Anagrafica_partitaIva presente nel CSV
    db_match_field = CSV_TO_DB_COLUMN_MAP.get(match_field, match_field)

    result = await session.execute(
        select(Item)
        .where(getattr(Item, db_match_field).in_(match_values))
        .order_by(Item.created_at.asc(), Item.id.asc())
    )
    items = result.scalars().all()

    items_by_match: dict[str, Item] = {}
    for item in items:
        key = getattr(item, db_match_field)
        if key not in items_by_match:
            items_by_match[key] = item

    changed_items_set: set[Item] = set()

    for row in csv_rows:
        key = row["match"]
        data = row["data"]

        target_item = items_by_match.get(key)
        if target_item:
            for field, value in data.items():
                setattr(target_item, field, value)
            target_item.updated_at = datetime.now(timezone.utc)
            changed_items_set.add(target_item)
            continue

        missing_required_for_insert = [
            col
            for col in required_insert_columns
            if data.get(col) is None
        ]
        if missing_required_for_insert:
            csv_cols = [DB_TO_CSV_COLUMN_MAP.get(col, col) for col in missing_required_for_insert]
            raise HTTPException(
                status_code=400,
                detail=(
                    "Impossibile inserire una nuova riga per "
                    f"{match_field}='{key}' (riga CSV {row['line_num']}): "
                    "mancano i campi obbligatori "
                    f"{', '.join(sorted(csv_cols))}."
                ),
            )

        new_item = Item(**data)
        session.add(new_item)
        items_by_match[key] = new_item
        changed_items_set.add(new_item)

    if not changed_items_set:
        raise HTTPException(
            status_code=400,
            detail="Il CSV non contiene modifiche da applicare.",
        )

    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Errore di integrità durante l'aggiornamento dei dati: {str(e.orig)}",
        )

    updated_items: list[Item] = []
    for item in changed_items_set:
        await session.refresh(item)
        updated_items.append(item)

    updated_items.sort(key=lambda it: it.created_at or datetime.min, reverse=True)

    return updated_items


# -------------------------------------------------------------------------
# READ single
# -------------------------------------------------------------------------
@router.get(
    "/{item_id}",
    response_model=ItemOut,
    dependencies=[Depends(require_levels("reader", "editor", "admin"))],
)
async def get_item(item_id: UUID, session: AsyncSession = Depends(get_session)):
    return await _get_or_404(session, item_id)


# -------------------------------------------------------------------------
# UPDATE (editor/admin)
# -------------------------------------------------------------------------
@router.put(
    "/{partita_iva}",
    response_model=ItemOut,
    dependencies=[Depends(require_levels("editor", "admin"))],
)
async def update_item(
    partita_iva: str,
    patch: ItemUpdate,
    session: AsyncSession = Depends(get_session),
):
    item = await _get_by_partita_iva_or_404(session, partita_iva)
    for field, value in patch.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    item.updated_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(item)
    return item

# -------------------------------------------------------------------------
# DELETE by row ID (admin)
# -------------------------------------------------------------------------
@router.delete(
    "/by-id/{item_id}",
    status_code=204,
    dependencies=[Depends(require_levels("admin"))],
)
async def delete_item_by_id(
    item_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    item = await _get_or_404(session, item_id)
    await session.delete(item)
    await session.commit()
    return {"status": "deleted", "id": str(item_id)}


# -------------------------------------------------------------------------
# DELETE by partita IVA (admin)
# -------------------------------------------------------------------------
@router.delete(
    "/{partita_iva}",
    status_code=204,
    dependencies=[Depends(require_levels("admin"))],
)
async def delete_item(
    partita_iva: str,
    session: AsyncSession = Depends(get_session),
):
    item = await _get_by_partita_iva_or_404(session, partita_iva)

    await session.delete(item)
    await session.commit()

    return {"status": "deleted", "PIVA": partita_iva}
