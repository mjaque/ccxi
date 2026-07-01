from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
SCHEMA_PATH = ROOT_DIR / "backend" / "schema.sql"

REQUIRED_TABLES = {
    "Metadatos",
    "Estudiante",
    "Resultado",
    "Indicador",
    "Actividad",
    "Indicador_Resultado",
    "Indicador_Actividad",
    "Calificacion",
}

_INVALID_ALREADY_REPORTED = set()


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def normalize_modulo(name: str) -> str:
    if name is None:
        raise ValueError("El nombre de la base de datos es obligatorio")

    name = str(name).strip()
    if name.endswith(".sqlite"):
        name = name[:-7]

    if not name:
        raise ValueError("El nombre de la base de datos es obligatorio")

    if "/" in name or "\\" in name or "\x00" in name:
        raise ValueError("El nombre de la base de datos no puede contener separadores de ruta")

    return name


def get_db_path(modulo: str) -> Path:
    return DATA_DIR / f"{normalize_modulo(modulo)}.sqlite"


def get_connection(modulo: str) -> sqlite3.Connection:
    ensure_data_dir()
    conn = sqlite3.connect(get_db_path(modulo))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    _migrar_modulo(conn)
    return conn


def _migrar_modulo(conn: sqlite3.Connection) -> None:
    migraciones = [
        """ALTER TABLE "Indicador_Actividad"
           ADD COLUMN "tipo_calificacion" TEXT NOT NULL DEFAULT 'ponderada'
           CHECK (tipo_calificacion IN ('ponderada', 'maxima', 'minima'))""",
        """ALTER TABLE "Indicador_Actividad"
           ADD COLUMN "peso" INTEGER CHECK (peso >= 0)""",
    ]
    for sql in migraciones:
        try:
            conn.execute(sql)
        except sqlite3.OperationalError:
            pass


def _validate_db_file(db_path: Path) -> tuple[bool, str]:
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
            """).fetchall()

            tables = {row["name"] for row in rows}
            missing = REQUIRED_TABLES - tables
            if missing:
                return False, f"faltan tablas: {', '.join(sorted(missing))}"

            row = conn.execute("""
                SELECT valor
                FROM "Metadatos"
                WHERE clave = 'app_name'
            """).fetchone()

            if row is None:
                return False, "falta el metadato app_name"

            if row["valor"] != "ccxi":
                return False, f"app_name no válido: {row['valor']}"

            return True, ""

    except sqlite3.DatabaseError as exc:
        return False, str(exc)


def list_valid_modulos() -> list[str]:
    ensure_data_dir()
    valid_names = []

    for db_path in sorted(DATA_DIR.glob("*.sqlite"), key=lambda p: p.name.lower()):
        ok, error = _validate_db_file(db_path)

        if ok:
            valid_names.append(db_path.stem)
        else:
            if db_path.name not in _INVALID_ALREADY_REPORTED:
                print(f"ERROR: base de datos inválida '{db_path.name}': {error}")
                _INVALID_ALREADY_REPORTED.add(db_path.name)

    return valid_names


def create_modulo(modulo: str) -> str:
    ensure_data_dir()
    modulo = normalize_modulo(modulo)
    db_path = get_db_path(modulo)

    if db_path.exists():
        raise FileExistsError("Ya existe una base de datos con ese nombre")

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        conn.commit()

    ok, error = _validate_db_file(db_path)
    if not ok:
        db_path.unlink(missing_ok=True)
        raise RuntimeError(f"No se pudo crear la base de datos: {error}")

    return modulo

