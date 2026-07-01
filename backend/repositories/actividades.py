from collections import defaultdict

from db import get_connection


def _replace_indicadores(conn, actividad_id: int, indicadores: list[dict]) -> None:
    conn.execute("""
        DELETE FROM "Indicador_Actividad"
        WHERE id_actividad = ?
    """, (actividad_id,))

    if indicadores:
        conn.executemany("""
            INSERT INTO "Indicador_Actividad" (id_indicador, id_actividad, tipo_calificacion, peso)
            VALUES (?, ?, ?, ?)
        """, [
            (item["id_indicador"], actividad_id,
             item.get("tipo_calificacion", "ponderada"),
             item.get("peso"))
            for item in indicadores
        ])


def _get_indicadores_por_actividad(conn) -> dict[int, list[dict]]:
    rows = conn.execute("""
        SELECT
            ip.id_actividad,
            i.id AS indicador_id,
            i.codigo AS indicador_codigo,
            i.nombre AS indicador_nombre,
            ip.tipo_calificacion,
            ip.peso
        FROM "Indicador_Actividad" ip
        JOIN "Indicador" i ON i.id = ip.id_indicador
        ORDER BY i.codigo COLLATE NOCASE ASC
    """).fetchall()

    indicadores_por_actividad = defaultdict(list)

    for row in rows:
        indicadores_por_actividad[row["id_actividad"]].append({
            "id": row["indicador_id"],
            "codigo": row["indicador_codigo"],
            "nombre": row["indicador_nombre"],
            "tipo_calificacion": row["tipo_calificacion"],
            "peso": row["peso"],
        })

    return indicadores_por_actividad


def list_actividades(modulo: str) -> list[dict]:
    with get_connection(modulo) as conn:
        actividades = [
            dict(row) for row in conn.execute("""
                SELECT id, codigo, nombre, fecha
                FROM "Actividad"
                ORDER BY fecha DESC, codigo COLLATE NOCASE ASC
            """).fetchall()
        ]

        indicadores_por_actividad = _get_indicadores_por_actividad(conn)

    for actividad in actividades:
        actividad["indicadores"] = indicadores_por_actividad.get(actividad["id"], [])

    return actividades


def get_actividad(modulo: str, actividad_id: int) -> dict | None:
    with get_connection(modulo) as conn:
        row = conn.execute("""
            SELECT id, codigo, nombre, fecha
            FROM "Actividad"
            WHERE id = ?
        """, (actividad_id,)).fetchone()

        if row is None:
            return None

        actividad = dict(row)
        indicadores_por_actividad = _get_indicadores_por_actividad(conn)
        actividad["indicadores"] = indicadores_por_actividad.get(actividad_id, [])

        return actividad


def create_actividad(modulo: str, codigo: str, nombre: str, fecha: str | None, indicadores: list[dict]) -> dict:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            INSERT INTO "Actividad" (codigo, nombre, fecha)
            VALUES (?, ?, ?)
        """, (codigo, nombre, fecha))
        actividad_id = cursor.lastrowid

        _replace_indicadores(conn, actividad_id, indicadores)
        conn.commit()

    actividad = get_actividad(modulo, actividad_id)
    if actividad is None:
        raise RuntimeError("No se pudo recuperar la actividad recién creada")

    return actividad


def update_actividad(modulo: str, actividad_id: int, codigo: str, nombre: str, fecha: str | None, indicadores: list[dict]) -> dict | None:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            UPDATE "Actividad"
            SET codigo = ?, nombre = ?, fecha = ?
            WHERE id = ?
        """, (codigo, nombre, fecha, actividad_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return None

        _replace_indicadores(conn, actividad_id, indicadores)
        conn.commit()

    return get_actividad(modulo, actividad_id)


def delete_actividad(modulo: str, actividad_id: int) -> bool:
    with get_connection(modulo) as conn:
        conn.execute("""
            DELETE FROM "Indicador_Actividad"
            WHERE id_actividad = ?
        """, (actividad_id,))

        cursor = conn.execute("""
            DELETE FROM "Actividad"
            WHERE id = ?
        """, (actividad_id,))
        conn.commit()

        return cursor.rowcount > 0
