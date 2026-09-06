from collections import defaultdict
from db import get_connection


def get_contexto_calificacion(modulo: str, actividad_id: int, estudiante_id: int | None = None) -> dict:
    estudiante_fk = estudiante_id if estudiante_id is not None else -1

    with get_connection(modulo) as conn:
        rows = conn.execute("""
            SELECT
                i.id AS id_indicador,
                i.codigo AS indicador_codigo,
                i.nombre AS indicador_nombre,
                CASE WHEN ia_check.id_indicador IS NOT NULL THEN 1 ELSE 0 END AS asociado,
                c.nivel_logro AS nivel_logro,
                c.incremento AS incremento
            FROM "Indicador" i
            LEFT JOIN "Indicador_Actividad" ia_check
                ON ia_check.id_indicador = i.id AND ia_check.id_actividad = ?
            INNER JOIN (
                SELECT id_indicador FROM "Indicador_Actividad" WHERE id_actividad = ?
                UNION
                SELECT id_indicador FROM "Calificacion" WHERE id_actividad = ? AND id_estudiante = ?
            ) ia ON ia.id_indicador = i.id
            LEFT JOIN "Calificacion" c
                ON c.id_indicador = i.id
               AND c.id_actividad = ?
               AND c.id_estudiante = ?
            ORDER BY i.codigo COLLATE NOCASE ASC
        """, (actividad_id, actividad_id, actividad_id, estudiante_fk, actividad_id, estudiante_fk)).fetchall()

        result = [dict(row) for row in rows]

        if estudiante_id is not None:
            actuales = _calcular_calificaciones_actuales(conn, estudiante_id)
            for row in result:
                row["calificacion_actual"] = actuales.get(row["id_indicador"])
        else:
            for row in result:
                row["calificacion_actual"] = None

        evaluacion = None
        if estudiante_id is not None:
            row = conn.execute('''
                SELECT evaluacion FROM "Evaluacion"
                WHERE id_estudiante = ? AND id_actividad = ?
            ''', (estudiante_id, actividad_id)).fetchone()
            evaluacion = row["evaluacion"] if row is not None else None

        return {"items": result, "evaluacion": evaluacion}


def _calcular_calificaciones_actuales(conn, estudiante_id: int) -> dict[int, float | None]:
    rows = conn.execute("""
        SELECT
            c.id_indicador,
            c.nivel_logro,
            c.incremento,
            ia.tipo_calificacion,
            ia.peso
        FROM "Calificacion" c
        LEFT JOIN "Indicador_Actividad" ia
            ON ia.id_indicador = c.id_indicador AND ia.id_actividad = c.id_actividad
        WHERE c.id_estudiante = ?
    """, (estudiante_id,)).fetchall()

    grupos = defaultdict(list)
    for row in rows:
        grupos[row["id_indicador"]].append(row)

    resultados = {}
    for id_indicador, items in grupos.items():
        maximas = [r["nivel_logro"] for r in items if r["tipo_calificacion"] == "maxima" and r["nivel_logro"] is not None]
        minimas = [r["nivel_logro"] for r in items if r["tipo_calificacion"] == "minima" and r["nivel_logro"] is not None]
        ponderadas = [(r["nivel_logro"], r["peso"] or 1)
                      for r in items if r["tipo_calificacion"] == "ponderada" and r["nivel_logro"] is not None]
        total_inc = sum(r["incremento"] for r in items if r["incremento"] is not None)

        if minimas:
            resultados[id_indicador] = float(max(minimas))
        elif maximas:
            max_of_max = float(max(maximas))
            if ponderadas:
                pond = sum(n * p for n, p in ponderadas) / sum(p for _, p in ponderadas)
                resultados[id_indicador] = min(max_of_max, pond) + total_inc
            else:
                resultados[id_indicador] = max_of_max + total_inc
        elif ponderadas:
            resultados[id_indicador] = sum(n * p for n, p in ponderadas) / sum(p for _, p in ponderadas) + total_inc
        else:
            resultados[id_indicador] = None

    return resultados


def guardar_calificacion(
    modulo: str,
    actividad_id: int,
    estudiante_id: int,
    items: list[dict],
    evaluacion: str | None,
) -> None:
    with get_connection(modulo) as conn:
        indicadores_existentes = {
            row["id"] for row in conn.execute(
                'SELECT id FROM "Indicador"'
            ).fetchall()
        }
        indicadores_payload = {item["id_indicador"] for item in items}

        if not indicadores_payload.issubset(indicadores_existentes):
            raise ValueError("Alguno de los indicadores no existe")

        conn.execute("""
            DELETE FROM "Calificacion"
            WHERE id_estudiante = ? AND id_actividad = ?
        """, (estudiante_id, actividad_id))

        filas = [
            (estudiante_id, item["id_indicador"], actividad_id, item["nivel_logro"], item["incremento"])
            for item in items
            if item["nivel_logro"] is not None or item["incremento"] is not None
        ]

        if filas:
            conn.executemany("""
                INSERT INTO "Calificacion"
                    (id_estudiante, id_indicador, id_actividad, nivel_logro, incremento)
                VALUES (?, ?, ?, ?, ?)
            """, filas)

        conn.execute('''
            INSERT INTO "Evaluacion" (id_estudiante, id_actividad, evaluacion)
            VALUES (?, ?, ?)
            ON CONFLICT (id_estudiante, id_actividad)
            DO UPDATE SET evaluacion = excluded.evaluacion
        ''', (estudiante_id, actividad_id, evaluacion))

        conn.commit()


def borrar_calificacion(modulo: str, actividad_id: int, estudiante_id: int) -> bool:
    with get_connection(modulo) as conn:
        cursor = conn.execute("""
            DELETE FROM "Calificacion"
            WHERE id_estudiante = ? AND id_actividad = ?
        """, (estudiante_id, actividad_id))
        evaluacion_cursor = conn.execute('''
            DELETE FROM "Evaluacion"
            WHERE id_estudiante = ? AND id_actividad = ?
        ''', (estudiante_id, actividad_id))
        conn.commit()
        return cursor.rowcount > 0 or evaluacion_cursor.rowcount > 0
