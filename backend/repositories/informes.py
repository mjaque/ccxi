import statistics
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


def _calcular_cuartiles(valores: list[float]) -> dict[str, float | None]:
    validos = sorted([v for v in valores if v is not None])
    if not validos:
        return {"q1": None, "q2": None, "q3": None}
    if len(validos) == 1:
        return {"q1": validos[0], "q2": validos[0], "q3": validos[0]}
    n = len(validos)
    q2 = statistics.median(validos)
    lower = validos[:n // 2]
    if n % 2 == 0:
        upper = validos[n // 2:]
    else:
        upper = validos[n // 2 + 1:]
    q1 = statistics.median(lower)
    q3 = statistics.median(upper)
    return {"q1": q1, "q2": q2, "q3": q3}


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


def get_listado_indicadores(modulo: str) -> dict:
    """Devuelve los indicadores agrupados por resultado de aprendizaje."""
    with get_connection(modulo) as conn:
        resultados, indicadores_por_resultado = _get_resultados_y_relaciones(conn)

        resultados_informe = []
        for resultado in resultados:
            indicadores = [
                {
                    "id": relacion["id_indicador"],
                    "codigo": relacion["indicador_codigo"],
                    "nombre": relacion["indicador_nombre"],
                    "peso": relacion["peso"],
                }
                for relacion in indicadores_por_resultado.get(resultado["id"], [])
            ]
            resultados_informe.append({
                "id": resultado["id"],
                "codigo": resultado["codigo"],
                "nombre": resultado["nombre"],
                "peso": resultado["peso"],
                "indicadores": indicadores,
            })

        return {
            "modulo": modulo,
            "resultados": resultados_informe,
        }


def _calcular_notas_alumno(conn, alumno_id: int, fecha_informe: str | None) -> dict:
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

    resultados_info = []
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

        indicadores_info = []
        for rel in relaciones:
            indicadores_info.append({
                "id_indicador": rel["id_indicador"],
                "codigo": rel["indicador_codigo"],
                "nombre": rel["indicador_nombre"],
                "peso": rel["peso"],
                "nota": notas_indicadores.get(rel["id_indicador"]),
            })

        resultados_info.append({
            "id": resultado["id"],
            "codigo": resultado["codigo"],
            "nombre": resultado["nombre"],
            "peso": resultado["peso"],
            "nota": nota_resultado,
            "indicadores": indicadores_info,
        })

    nota_final = None
    if suma_pesos_final > 0:
        nota_final = suma_ponderada_final / suma_pesos_final

    return {
        "notas_indicadores": notas_indicadores,
        "notas_resultados": {r["id"]: r["nota"] for r in resultados_info},
        "nota_final": nota_final,
        "resultados_info": resultados_info,
    }


def _calcular_resultados_alumno(conn, alumno_id: int, fecha_informe: str | None) -> dict[int, float]:
    return _calcular_notas_alumno(conn, alumno_id, fecha_informe)["notas_resultados"]


def get_informe_alumnado(modulo: str, alumno_id: int, fecha_informe: str | None = None) -> dict:
    with get_connection(modulo) as conn:
        alumno = conn.execute("""
            SELECT id, nombre
            FROM Estudiante
            WHERE id = ?
        """, (alumno_id,)).fetchone()

        if alumno is None:
            raise ValueError("El alumno seleccionado no existe")

        filtro_fecha, params_fecha = _build_fecha_filter("a", fecha_informe)

        datos_alumno = _calcular_notas_alumno(conn, alumno_id, fecha_informe)
        resultados_informe = datos_alumno["resultados_info"]
        nota_final = datos_alumno["nota_final"]

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


def _calcular_actividades_por_resultado(conn, alumno_id: int, fecha_informe: str | None) -> dict[int, dict]:
    filtro_fecha, params_fecha = _build_fecha_filter("a", fecha_informe)

    rows = [
        dict(row) for row in conn.execute(f"""
            SELECT
                r.id AS resultado_id,
                r.codigo AS resultado_codigo,
                r.nombre AS resultado_nombre,
                a.id AS actividad_id,
                a.codigo AS actividad_codigo,
                a.nombre AS actividad_nombre,
                a.fecha AS actividad_fecha,
                i.id AS indicador_id,
                ir.peso AS ir_peso,
                ia.tipo_calificacion,
                ia.peso AS ia_peso,
                c.nivel_logro,
                c.incremento
            FROM "Resultado" r
            JOIN "Indicador_Resultado" ir ON ir.id_resultado = r.id
            JOIN "Indicador" i ON i.id = ir.id_indicador
            JOIN "Indicador_Actividad" ia ON ia.id_indicador = i.id
            JOIN "Actividad" a ON a.id = ia.id_actividad
            LEFT JOIN "Calificacion" c
                ON c.id_actividad = a.id
                AND c.id_indicador = i.id
                AND c.id_estudiante = ?
            WHERE {filtro_fecha}
            ORDER BY r.codigo COLLATE NOCASE ASC,
                a.fecha ASC,
                a.codigo COLLATE NOCASE ASC,
                i.codigo COLLATE NOCASE ASC
        """, (alumno_id, *params_fecha)).fetchall()
    ]

    resultados_map: dict[int, dict] = {}
    for row in rows:
        res_id = row["resultado_id"]
        if res_id not in resultados_map:
            resultados_map[res_id] = {
                "id": res_id,
                "codigo": row["resultado_codigo"],
                "nombre": row["resultado_nombre"],
                "actividades": {},
            }

        act_id = row["actividad_id"]
        if act_id not in resultados_map[res_id]["actividades"]:
            resultados_map[res_id]["actividades"][act_id] = {
                "id": act_id,
                "codigo": row["actividad_codigo"],
                "nombre": row["actividad_nombre"],
                "fecha": row["actividad_fecha"],
                "tipo_calificacion": row["tipo_calificacion"],
                "peso": row["ia_peso"],
                "items": [],
            }

        nivel = row["nivel_logro"]
        nota = None
        if nivel is not None:
            nota = _clamp_nota_indicador(
                float(nivel) + float(row["incremento"] or 0)
            )

        resultados_map[res_id]["actividades"][act_id]["items"].append({
            "peso": row["ir_peso"],
            "nota": nota,
        })

    for res_data in resultados_map.values():
        for act_data in res_data["actividades"].values():
            numerador = 0.0
            denominador = 0.0
            for item in act_data["items"]:
                if item["nota"] is not None:
                    numerador += item["nota"] * item["peso"]
                    denominador += item["peso"]

            act_data["calificacion"] = numerador / denominador if denominador > 0 else None
            del act_data["items"]

    return resultados_map


def get_informe_actividades_por_resultados(
    modulo: str, alumno_id: int, fecha_informe: str | None = None
) -> dict:
    with get_connection(modulo) as conn:
        alumno = conn.execute("""
            SELECT id, nombre
            FROM Estudiante
            WHERE id = ?
        """, (alumno_id,)).fetchone()

        if alumno is None:
            raise ValueError("El alumno seleccionado no existe")

        resultados_map = _calcular_actividades_por_resultado(conn, alumno_id, fecha_informe)

        datos_alumno = _calcular_notas_alumno(conn, alumno_id, fecha_informe)
        resultados_notas_map = datos_alumno["notas_resultados"]
        nota_final = datos_alumno["nota_final"]

        resultados_list = []
        for res_id in sorted(resultados_map, key=lambda x: resultados_map[x]["codigo"]):
            res_data = resultados_map[res_id]

            actividades_ordenadas = sorted(
                res_data["actividades"].values(),
                key=lambda a: (a["fecha"] or "", a["codigo"])
            )

            resultados_list.append({
                "id": res_data["id"],
                "codigo": res_data["codigo"],
                "nombre": res_data["nombre"],
                "nota": resultados_notas_map.get(res_id),
                "actividades": actividades_ordenadas,
            })

        return {
            "modulo": modulo,
            "fecha_informe": fecha_informe,
            "estudiante": dict(alumno),
            "nota_final": nota_final,
            "resultados": resultados_list,
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

        if not alumnos:
            return {
                "modulo": modulo,
                "fecha_informe": fecha_informe,
                "numero_estudiantes": 0,
                "nota_final": None,
                "resultados": [],
            }

        resultados_metadata, indicadores_por_resultado = _get_resultados_y_relaciones(conn)

        notas_finales: list[float] = []
        notas_por_resultado: dict[int, list[float]] = defaultdict(list)
        notas_por_indicador: dict[int, list[float]] = defaultdict(list)

        for alumno in alumnos:
            datos = _calcular_notas_alumno(conn, alumno["id"], fecha_informe)

            if datos["nota_final"] is not None:
                notas_finales.append(datos["nota_final"])

            for id_res, nota in datos["notas_resultados"].items():
                if nota is not None:
                    notas_por_resultado[id_res].append(nota)

            for id_ind, nota in datos["notas_indicadores"].items():
                notas_por_indicador[id_ind].append(nota)

        resultados_informe = []

        for resultado in resultados_metadata:
            relaciones = indicadores_por_resultado.get(resultado["id"], [])

            indicadores_informe = []
            for rel in relaciones:
                notas_ind = notas_por_indicador.get(rel["id_indicador"], [])
                indicadores_informe.append({
                    "id_indicador": rel["id_indicador"],
                    "codigo": rel["indicador_codigo"],
                    "nombre": rel["indicador_nombre"],
                    "peso": rel["peso"],
                    "nota": _calcular_cuartiles(notas_ind),
                })

            notas_res = notas_por_resultado.get(resultado["id"], [])
            resultados_informe.append({
                "id": resultado["id"],
                "codigo": resultado["codigo"],
                "nombre": resultado["nombre"],
                "peso": resultado["peso"],
                "nota": _calcular_cuartiles(notas_res),
                "indicadores": indicadores_informe,
            })

        return {
            "modulo": modulo,
            "fecha_informe": fecha_informe,
            "numero_estudiantes": len(alumnos),
            "nota_final": _calcular_cuartiles(notas_finales),
            "resultados": resultados_informe,
        }


def get_informe_actividades_por_resultados_grupo(
    modulo: str, fecha_informe: str | None = None
) -> dict:
    with get_connection(modulo) as conn:
        alumnos = [
            dict(row) for row in conn.execute("""
                SELECT id, nombre
                FROM Estudiante
                ORDER BY nombre COLLATE NOCASE ASC
            """).fetchall()
        ]

        if not alumnos:
            return {
                "modulo": modulo,
                "fecha_informe": fecha_informe,
                "numero_estudiantes": 0,
                "nota_final": None,
                "resultados": [],
            }

        notas_finales: list[float] = []
        notas_por_resultado: dict[int, list[float]] = defaultdict(list)
        calificaciones_por_actividad: dict[tuple[int, int], list[float]] = defaultdict(list)
        metadata: dict[int, dict] = {}

        for alumno in alumnos:
            datos = _calcular_notas_alumno(conn, alumno["id"], fecha_informe)
            act_map = _calcular_actividades_por_resultado(conn, alumno["id"], fecha_informe)

            if datos["nota_final"] is not None:
                notas_finales.append(datos["nota_final"])

            for id_res, nota in datos["notas_resultados"].items():
                if nota is not None:
                    notas_por_resultado[id_res].append(nota)

            for res_id, res_data in act_map.items():
                if res_id not in metadata:
                    metadata[res_id] = {
                        "id": res_id,
                        "codigo": res_data["codigo"],
                        "nombre": res_data["nombre"],
                        "actividades": {},
                    }
                for act_id, act_data in res_data["actividades"].items():
                    if act_id not in metadata[res_id]["actividades"]:
                        metadata[res_id]["actividades"][act_id] = {
                            "id": act_id,
                            "codigo": act_data["codigo"],
                            "nombre": act_data["nombre"],
                            "fecha": act_data["fecha"],
                            "tipo_calificacion": act_data["tipo_calificacion"],
                            "peso": act_data["peso"],
                        }
                    if act_data["calificacion"] is not None:
                        calificaciones_por_actividad[(res_id, act_id)].append(act_data["calificacion"])

        resultados_list = []
        for res_id in sorted(metadata, key=lambda x: metadata[x]["codigo"]):
            res_data = metadata[res_id]

            notas_res = notas_por_resultado.get(res_id, [])
            actividades_list = []
            for act_id in sorted(
                res_data["actividades"],
                key=lambda a: (res_data["actividades"][a]["fecha"] or "", res_data["actividades"][a]["codigo"])
            ):
                act_data = res_data["actividades"][act_id]
                califs = calificaciones_por_actividad.get((res_id, act_id), [])
                actividades_list.append({
                    "id": act_data["id"],
                    "codigo": act_data["codigo"],
                    "nombre": act_data["nombre"],
                    "fecha": act_data["fecha"],
                    "tipo_calificacion": act_data["tipo_calificacion"],
                    "peso": act_data["peso"],
                    "calificacion": _calcular_cuartiles(califs),
                })

            resultados_list.append({
                "id": res_data["id"],
                "codigo": res_data["codigo"],
                "nombre": res_data["nombre"],
                "nota": _calcular_cuartiles(notas_res),
                "actividades": actividades_list,
            })

        return {
            "modulo": modulo,
            "fecha_informe": fecha_informe,
            "numero_estudiantes": len(alumnos),
            "nota_final": _calcular_cuartiles(notas_finales),
            "resultados": resultados_list,
        }
