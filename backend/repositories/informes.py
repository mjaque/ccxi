import math
from collections import defaultdict
from db import get_connection


def _build_fecha_filter(alias_prueba: str, fecha_informe: str | None) -> tuple[str, list]:
    clauses = [f'{alias_prueba}.fecha IS NOT NULL']
    params: list = []

    if fecha_informe:
        clauses.append(f'{alias_prueba}.fecha <= ?')
        params.append(fecha_informe)

    return " AND ".join(clauses), params


def _clamp_nota_indicador(valor: float) -> float:
    if valor < 1:
        return 1.0
    if valor > 10:
        return 10.0
    return valor


def _calcular_notas_indicadores(rows: list[dict]) -> dict[int, float]:
    por_indicador: dict[int, list[dict]] = defaultdict(list)

    for row in rows:
        por_indicador[row["id_indicador"]].append(row)

    notas: dict[int, float] = {}

    for id_indicador, items in por_indicador.items():
        niveles = [item for item in items if item["nivel_logro"] is not None]
        if not niveles:
            continue

        max_nivel = max(item["nivel_logro"] for item in niveles)
        fecha_base = max(item["fecha"] for item in niveles if item["nivel_logro"] == max_nivel)

        incremento_total = sum(
            float(item["incremento"] or 0)
            for item in items
            if item["fecha"] > fecha_base
        )

        nota = _clamp_nota_indicador(float(max_nivel) + incremento_total)
        notas[id_indicador] = nota

    return notas


def _get_resultados_y_relaciones(conn) -> tuple[list[dict], dict[int, list[dict]]]:
    resultados = [
        dict(row) for row in conn.execute("""
            SELECT id, codigo, nombre, peso
            FROM "Resultado"
            ORDER BY codigo COLLATE NOCASE ASC
        """).fetchall()
    ]

    relaciones_resultado = [
        dict(row) for row in conn.execute("""
            SELECT
                ir.id_resultado,
                ir.id_indicador,
                ir.peso,
                i.codigo AS indicador_codigo,
                i.nombre AS indicador_nombre
            FROM "Indicador_Resultado" ir
            JOIN "Indicador" i ON i.id = ir.id_indicador
            ORDER BY ir.id_resultado, i.codigo COLLATE NOCASE ASC
        """).fetchall()
    ]

    indicadores_por_resultado: dict[int, list[dict]] = defaultdict(list)
    for row in relaciones_resultado:
        indicadores_por_resultado[row["id_resultado"]].append(row)

    return resultados, indicadores_por_resultado


def _calcular_resultados_alumno(conn, alumno_id: int, fecha_informe: str | None) -> dict[int, float]:
    resultados, indicadores_por_resultado = _get_resultados_y_relaciones(conn)
    filtro_fecha, params_fecha = _build_fecha_filter("a", fecha_informe)

    rows_calculo = [
        dict(row) for row in conn.execute(f"""
            SELECT
                c.id_indicador,
                c.nivel_logro,
                c.incremento,
                a.fecha
            FROM "Calificacion" c
            JOIN "Actividad" a ON a.id = c.id_actividad
            WHERE c.id_estudiante = ?
              AND {filtro_fecha}
            ORDER BY a.fecha ASC, c.id_actividad ASC, c.id_indicador ASC
        """, (alumno_id, *params_fecha)).fetchall()
        ]

    notas_indicadores = _calcular_notas_indicadores(rows_calculo)
    notas_resultado: dict[int, float] = {}

    for resultado in resultados:
        relaciones = indicadores_por_resultado.get(resultado["id"], [])

        numerador = 0.0
        denominador = 0.0

        for rel in relaciones:
            nota_indicador = notas_indicadores.get(rel["id_indicador"])
            if nota_indicador is None:
                continue

            peso_indicador = float(rel["peso"])
            numerador += nota_indicador * peso_indicador
            denominador += peso_indicador

        if denominador > 0:
            notas_resultado[resultado["id"]] = numerador / denominador

    return notas_resultado


def get_informe_alumnado(modulo: str, alumno_id: int, fecha_informe: str | None = None) -> dict:
    with get_connection(modulo) as conn:
        alumno = conn.execute("""
            SELECT id, nombre
            FROM Estudiante
            WHERE id = ?
        """, (alumno_id,)).fetchone()

        if alumno is None:
            raise ValueError("El alumno seleccionado no existe")

        resultados, indicadores_por_resultado = _get_resultados_y_relaciones(conn)

        filtro_fecha, params_fecha = _build_fecha_filter("a", fecha_informe)

        rows_calculo = [
            dict(row) for row in conn.execute(f"""
                SELECT
                    c.id_indicador,
                    c.nivel_logro,
                    c.incremento,
                    a.fecha
                FROM "Calificacion" c
                JOIN "Actividad" a ON a.id = c.id_actividad
                WHERE c.id_estudiante = ?
                  AND {filtro_fecha}
                ORDER BY a.fecha ASC, c.id_actividad ASC, c.id_indicador ASC
            """, (alumno_id, *params_fecha)).fetchall()
        ]

        notas_indicadores = _calcular_notas_indicadores(rows_calculo)

        resultados_informe = []
        suma_ponderada_final = 0.0
        suma_pesos_final = 0.0

        for resultado in resultados:
            relaciones = indicadores_por_resultado.get(resultado["id"], [])

            numerador = 0.0
            denominador = 0.0

            for rel in relaciones:
                nota_indicador = notas_indicadores.get(rel["id_indicador"])
                if nota_indicador is None:
                    continue

                peso_indicador = float(rel["peso"])
                numerador += nota_indicador * peso_indicador
                denominador += peso_indicador

            nota_resultado = None
            if denominador > 0:
                nota_resultado = numerador / denominador
                peso_resultado = float(resultado["peso"])
                suma_ponderada_final += nota_resultado * peso_resultado
                suma_pesos_final += peso_resultado

            indicadores_informe = []
            for rel in relaciones:
                indicadores_informe.append({
                    "id_indicador": rel["id_indicador"],
                    "codigo": rel["indicador_codigo"],
                    "nombre": rel["indicador_nombre"],
                    "peso": rel["peso"],
                    "nota": notas_indicadores.get(rel["id_indicador"]),
                })

            resultados_informe.append({
                "id": resultado["id"],
                "codigo": resultado["codigo"],
                "nombre": resultado["nombre"],
                "peso": resultado["peso"],
                "nota": nota_resultado,
                "indicadores": indicadores_informe,
            })

        nota_final = None
        if suma_pesos_final > 0:
            nota_final = suma_ponderada_final / suma_pesos_final

        detalles = [
            dict(row) for row in conn.execute(f"""
                SELECT
                    a.id AS actividad_id,
                    a.codigo AS actividad_codigo,
                    a.nombre AS actividad_nombre,
                    a.fecha AS actividad_fecha,
                    i.codigo AS indicador_codigo,
                    i.nombre AS indicador_nombre,
                    COALESCE((
                        SELECT group_concat(r.codigo || ' (' || ir2.peso || ')', ', ')
                        FROM "Indicador_Resultado" ir2
                        JOIN "Resultado" r ON r.id = ir2.id_resultado
                        WHERE ir2.id_indicador = i.id
                    ), '—') AS pesos_resultado,
                    c.nivel_logro,
                    c.incremento
                FROM "Actividad" a
                JOIN "Indicador_Actividad" ia ON ia.id_actividad = a.id
                JOIN "Indicador" i ON i.id = ia.id_indicador
                LEFT JOIN "Calificacion" c
                    ON c.id_actividad = a.id
                   AND c.id_indicador = i.id
                   AND c.id_estudiante = ?
                WHERE {filtro_fecha}
                ORDER BY a.fecha ASC, a.codigo COLLATE NOCASE ASC, i.codigo COLLATE NOCASE ASC
            """, (alumno_id, *params_fecha)).fetchall()
        ]

        actividades_detalle: dict[int, dict] = {}
        for row in detalles:
            actividad_id = row["actividad_id"]

            if actividad_id not in actividades_detalle:
                actividades_detalle[actividad_id] = {
                    "id": actividad_id,
                    "codigo": row["actividad_codigo"],
                    "nombre": row["actividad_nombre"],
                    "fecha": row["actividad_fecha"],
                    "items": [],
                }

            actividades_detalle[actividad_id]["items"].append({
                "indicador_codigo": row["indicador_codigo"],
                "indicador_nombre": row["indicador_nombre"],
                "pesos_resultado": row["pesos_resultado"],
                "nivel_logro": row["nivel_logro"],
                "incremento": row["incremento"],
            })

        return {
            "modulo": modulo,
            "fecha_informe": fecha_informe,
			"estudiante": dict(alumno),
            "nota_final": nota_final,
            "resultados": resultados_informe,
            "actividades": list(actividades_detalle.values()),
        }


def get_informe_grupo(modulo: str, fecha_informe: str | None = None) -> dict:
    with get_connection(modulo) as conn:
        alumnos = [
            dict(row) for row in conn.execute("""
                SELECT id, nombre
                FROM Estudiante
                ORDER BY nombre COLLATE NOCASE ASC
            """).fetchall()
        ]

        resultados, _ = _get_resultados_y_relaciones(conn)

        notas_por_resultado: dict[int, list[float]] = defaultdict(list)

        for alumno in alumnos:
            notas_resultado_alumno = _calcular_resultados_alumno(conn, alumno["id"], fecha_informe)

            for id_resultado, nota in notas_resultado_alumno.items():
                notas_por_resultado[id_resultado].append(nota)

        resultados_informe = []

        for resultado in resultados:
            notas = notas_por_resultado.get(resultado["id"], [])

            if notas:
                media = sum(notas) / len(notas)
                varianza = sum((nota - media) ** 2 for nota in notas) / len(notas)
                desviacion_tipica = math.sqrt(varianza)
            else:
                media = None
                desviacion_tipica = None

            resultados_informe.append({
                "id": resultado["id"],
                "codigo": resultado["codigo"],
                "nombre": resultado["nombre"],
                "media": media,
                "desviacion_tipica": desviacion_tipica,
            })

        return {
            "modulo": modulo,
            "fecha_informe": fecha_informe,
            "resultados": resultados_informe,
        }
