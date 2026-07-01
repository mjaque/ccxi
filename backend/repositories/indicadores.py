from collections import defaultdict

from db import get_connection


def _replace_resultados(conn, indicador_id: int, resultados: list[dict]) -> None:
    conn.execute("""
        DELETE FROM "Indicador_Resultado"
        WHERE id_indicador = ?
    """, (indicador_id,))

    if resultados:
        conn.executemany("""
            INSERT INTO "Indicador_Resultado" (id_indicador, id_resultado, peso)
            VALUES (?, ?, ?)
        """, [
            (indicador_id, item["id_resultado"], item["peso"])
            for item in resultados
        ])


def _get_resultados_por_indicador(conn) -> dict[int, list[dict]]:
    rows = conn.execute("""
        SELECT
            ir.id_indicador,
            r.id AS resultado_id,
            r.codigo AS resultado_codigo,
            r.nombre AS resultado_nombre,
            ir.peso AS peso
        FROM "Indicador_Resultado" ir
        JOIN "Resultado" r ON r.id = ir.id_resultado
        ORDER BY r.codigo COLLATE NOCASE ASC
    """).fetchall()

    resultados_por_indicador = defaultdict(list)

    for row in rows:
        resultados_por_indicador[row["id_indicador"]].append({
            "id": row["resultado_id"],
            "codigo": row["resultado_codigo"],
            "nombre": row["resultado_nombre"],
            "peso": row["peso"],
        })

    return resultados_por_indicador


def list_indicadores(modulo: str) -> list[dict]:
    with get_connection(modulo) as conn:
        indicadores = [
            dict(row) for row in conn.execute("""
                SELECT id, codigo, nombre
                FROM "Indicador"
                ORDER BY codigo COLLATE NOCASE ASC
            """).fetchall()
        ]

        resultados_por_indicador = _get_resultados_por_indicador(conn)

    for indicador in indicadores:
        resultados = resultados_por_indicador.get(indicador["id"], [])
        indicador["resultados"] = resultados

    return indicadores


def get_indicador(modulo: str, indicador_id: int) -> dict | None:
    with get_connection(modulo) as conn:
        row = conn.execute("""
            SELECT id, codigo, nombre
            FROM "Indicador"
            WHERE id = ?
        """, (indicador_id,)).fetchone()

        if row is None:
            return None

        indicador = dict(row)
        resultados_por_indicador = _get_resultados_por_indicador(conn)
        indicador["resultados"] = resultados_por_indicador.get(indicador_id, [])

        return indicador


def create_indicador(modulo: str, codigo: str, nombre: str, resultados: list[dict]) -> dict:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            INSERT INTO "Indicador" (codigo, nombre)
            VALUES (?, ?)
        """, (codigo, nombre))
        indicador_id = cursor.lastrowid

        _replace_resultados(conn, indicador_id, resultados)
        conn.commit()

    indicador = get_indicador(modulo, indicador_id)
    if indicador is None:
        raise RuntimeError("No se pudo recuperar el indicador recién creado")

    return indicador


def update_indicador(modulo: str, indicador_id: int, codigo: str, nombre: str, resultados: list[dict]) -> dict | None:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            UPDATE "Indicador"
            SET codigo = ?, nombre = ?
            WHERE id = ?
        """, (codigo, nombre, indicador_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return None

        _replace_resultados(conn, indicador_id, resultados)
        conn.commit()

    return get_indicador(modulo, indicador_id)


def delete_indicador(modulo: str, indicador_id: int) -> bool:
    with get_connection(modulo) as conn:
        conn.execute("""
            DELETE FROM "Indicador_Resultado"
            WHERE id_indicador = ?
        """, (indicador_id,))

        cursor = conn.execute("""
            DELETE FROM "Indicador"
            WHERE id = ?
        """, (indicador_id,))
        conn.commit()

        return cursor.rowcount > 0

def search_indicadores(modulo: str, query: str, limit: int = 15) -> list[dict]:
    patron = f"%{query.strip()}%"

    with get_connection(modulo) as conn:
        rows = conn.execute("""
            SELECT id, codigo, nombre
            FROM "Indicador"
            WHERE codigo LIKE ? OR nombre LIKE ?
            ORDER BY codigo COLLATE NOCASE ASC
            LIMIT ?
        """, (patron, patron, limit)).fetchall()

        return [dict(row) for row in rows]

