from db import get_connection

def list_estudiantes(modulo: str) -> list[dict]:
    with get_connection(modulo) as conn:
        rows = conn.execute("""
            SELECT id, nombre
            FROM Estudiante
            ORDER BY nombre COLLATE NOCASE ASC
        """).fetchall()
        return [dict(row) for row in rows]


def get_estudiante(modulo: str, estudiante_id: int) -> dict | None:
    with get_connection(modulo) as conn:
        row = conn.execute("""
            SELECT id, nombre
            FROM Estudiante
            WHERE id = ?
        """, (estudiante_id,)).fetchone()
        return dict(row) if row else None


def create_estudiante(modulo: str, nombre: str) -> dict:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            INSERT INTO Estudiante (nombre)
            VALUES (?)
        """, (nombre,))
        conn.commit()
        estudiante_id = cursor.lastrowid

    estudiante = get_estudiante(modulo, estudiante_id)
    if estudiante is None:
        raise RuntimeError("No se pudo recuperar el estudiante recién creado")
    return estudiante


def update_estudiante(modulo: str, estudiante_id: int, nombre: str) -> dict | None:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            UPDATE Estudiante
            SET nombre = ?
            WHERE id = ?
        """, (nombre, estudiante_id))
        conn.commit()

        if cursor.rowcount == 0:
            return None

    return get_estudiante(modulo, estudiante_id)


def delete_estudiante(modulo: str, estudiante_id: int) -> bool:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            DELETE FROM Estudiante
            WHERE id = ?
        """, (estudiante_id,))
        conn.commit()
        return cursor.rowcount > 0
