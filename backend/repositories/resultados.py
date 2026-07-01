from db import get_connection


def list_resultados(modulo: str) -> list[dict]:
    with get_connection(modulo) as conn:
        rows = conn.execute("""
            SELECT id, codigo, nombre, peso
            FROM "Resultado"
            ORDER BY codigo COLLATE NOCASE ASC
        """).fetchall()
        return [dict(row) for row in rows]


def get_resultado(modulo: str, resultado_id: int) -> dict | None:
    with get_connection(modulo) as conn:
        row = conn.execute("""
            SELECT id, codigo, nombre, peso
            FROM "Resultado"
            WHERE id = ?
        """, (resultado_id,)).fetchone()
        return dict(row) if row else None


def create_resultado(modulo: str, codigo: str, nombre: str, peso: int) -> dict:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            INSERT INTO "Resultado" (codigo, nombre, peso)
            VALUES (?, ?, ?)
        """, (codigo, nombre, peso))
        conn.commit()
        resultado_id = cursor.lastrowid

    resultado = get_resultado(modulo, resultado_id)
    if resultado is None:
        raise RuntimeError("No se pudo recuperar el resultado recién creado")
    return resultado


def update_resultado(modulo: str, resultado_id: int, codigo: str, nombre: str, peso: int) -> dict | None:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            UPDATE "Resultado"
            SET codigo = ?, nombre = ?, peso = ?
            WHERE id = ?
        """, (codigo, nombre, peso, resultado_id))
        conn.commit()

        if cursor.rowcount == 0:
            return None

    return get_resultado(modulo, resultado_id)


def delete_resultado(modulo: str, resultado_id: int) -> bool:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            DELETE FROM "Resultado"
            WHERE id = ?
        """, (resultado_id,))
        conn.commit()
        return cursor.rowcount > 0
