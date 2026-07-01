from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from datetime import date
from db import ensure_data_dir, list_valid_modulos, create_modulo, normalize_modulo
import json
import sqlite3

from controladores.principal import ControladorPrincipal

from repositories.estudiantes import (
    list_estudiantes,
    create_estudiante,
    update_estudiante,
    delete_estudiante,
)
from repositories.actividades import (
    list_actividades,
    create_actividad,
    update_actividad,
    delete_actividad,
)
from repositories.resultados import (
    list_resultados,
    create_resultado,
    update_resultado,
    delete_resultado,
)
from repositories.indicadores import (
    list_indicadores,
    create_indicador,
    update_indicador,
    delete_indicador,
    search_indicadores,
)
from repositories.calificaciones import (
    get_contexto_calificacion,
    guardar_calificacion,
    borrar_calificacion,
)
from repositories.informes import get_informe_alumnado, get_informe_grupo


ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
HOST = "127.0.0.1"
PORT = 8000

'''
    Manejador de peticiones RESTful
'''
class CCXIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self.path = "/html/index.html"
            '''
            controlador = ControladorPrincipal()
            html = controlador.getHTML()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return
            '''

        if path == "/api/health":
            self._send_json({
                "ok": True,
                "app": "ccxi",
                "message": "Servidor funcionando correctamente"
            })
            return

        if path == "/api/modulos":
            self._send_json({
                "ok": True,
                "items": [{"name": name} for name in list_valid_modulos()]
            })
            return

        if path == "/api/estudiantes":
            modulo = self._get_modulo()
            if modulo is None:
                return

            self._send_json({
                "ok": True,
                "items": list_estudiantes(modulo)
            })
            return

        if path == "/api/actividades":
            modulo = self._get_modulo()
            if modulo is None:
                return

            self._send_json({
                "ok": True,
                "items": list_actividades(modulo)
            })
            return

        if path == "/api/resultados":
            modulo = self._get_modulo()
            if modulo is None:
                return

            self._send_json({
                "ok": True,
                "items": list_resultados(modulo)
            })
            return

        if path == "/api/indicadores":
            modulo = self._get_modulo()
            if modulo is None:
                return

            self._send_json({
                "ok": True,
                "items": list_indicadores(modulo)
            })
            return

        if path == "/api/indicadores/buscar":
            modulo = self._get_modulo()
            if modulo is None:
                return

            query = parse_qs(parsed.query).get("q", [""])[0].strip()

            if len(query) < 2:
                self._send_json({
                    "ok": True,
                    "items": []
                })
                return

            self._send_json({
                "ok": True,
                "items": search_indicadores(modulo, query)
            })
            return

        if path == "/api/calificaciones/contexto":
            modulo = self._get_modulo()
            if modulo is None:
                return

            params = parse_qs(parsed.query)

            actividad_id = self._read_optional_positive_int(params.get("actividad_id"))
            estudiante_id = self._read_optional_positive_int(params.get("estudiante_id"))

            if actividad_id is None:
                self._send_json({
                    "ok": False,
                    "error": "Debes indicar una actividad válida"
                }, status=400)
                return

            self._send_json({
                "ok": True,
                "items": get_contexto_calificacion(modulo, actividad_id, estudiante_id)
            })
            return
           
        if path == "/api/informes/estudiantes":
            modulo = self._get_modulo()
            if modulo is None:
                return

            params = parse_qs(parsed.query)
            estudiante_id = self._read_optional_positive_int(params.get("estudiante_id"))
            fecha_informe = (params.get("fecha_informe", [""])[0] or "").strip() or None

            if estudiante_id is None:
                self._send_json({
                    "ok": False,
                    "error": "Debes seleccionar un estudiante"
                }, status=400)
                return

            if fecha_informe:
                try:
                    date.fromisoformat(fecha_informe)
                except ValueError:
                    self._send_json({
                        "ok": False,
                        "error": "La fecha del informe no es válida"
                    }, status=400)
                    return

            try:
                informe = get_informe_alumnado(modulo, estudiante_id, fecha_informe)
            except ValueError as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=400)
                return

            self._send_json({
                "ok": True,
                "item": informe
            })
            return

        if path == "/api/informes/grupo":
            modulo = self._get_modulo()
            if modulo is None:
                return

            params = parse_qs(parsed.query)
            fecha_informe = (params.get("fecha_informe", [""])[0] or "").strip() or None

            if fecha_informe:
                try:
                    date.fromisoformat(fecha_informe)
                except ValueError:
                    self._send_json({
                        "ok": False,
                        "error": "La fecha del informe no es válida"
                    }, status=400)
                    return

            informe = get_informe_grupo(modulo, fecha_informe)

            self._send_json({
                "ok": True,
                "item": informe
            })
            return
        return super().do_GET()


    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/modulos":
            data = self._read_json_body()
            nombre = (data.get("nombre") or "").strip()

            if not nombre:
                self._send_json({
                    "ok": False,
                    "error": "Debes indicar el nombre de la nueva base de datos"
                }, status=400)
                return

            try:
                modulo = create_modulo(nombre)
            except FileExistsError as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=400)
                return
            except (ValueError, RuntimeError) as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=400)
                return

            self._send_json({
                "ok": True,
                "item": {"name": modulo}
            }, status=201)
            return

        if path == "/api/estudiantes":
            modulo = self._get_modulo()
            if modulo is None:
                return

            data = self._read_json_body()
            estudiante = data.get("estudiante") or ""
            if not estudiante:
                self._send_json({
                    "ok": False,
                    "error": "No se ha recibido un estudiante válido."
                }, status=400)
                return

            nombre = (estudiante.get('nombre') or "").strip()

            if not nombre:
                self._send_json({
                    "ok": False,
                    "error": "El nombre es obligatorio"
                }, status=400)
                return

            try:
                estudiante = create_estudiante(modulo, nombre)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "Ya existe un estudiante con ese nombre"
                }, status=400)
                return

            self._send_json({
                "ok": True,
                "item": estudiante
            }, status=201)
            return

        if path == "/api/actividades":
            modulo = self._get_modulo()
            if modulo is None:
                return

            data = self._read_json_body()
            codigo = (data.get("codigo") or "").strip()
            nombre = (data.get("nombre") or "").strip()
            fecha_raw = (data.get("fecha") or "").strip()
            fecha = fecha_raw if fecha_raw else None
            indicadores = self._read_indicadores(data.get("indicadores"))

            error = self._validar_actividad(modulo, codigo, nombre, fecha, indicadores)
            if error:
                self._send_json({"ok": False, "error": error}, status=400)
                return

            try:
                actividad = create_actividad(modulo, codigo, nombre, fecha, indicadores)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se pudo crear la actividad. Revisa el código y las asociaciones con indicadores"
                }, status=400)
                return

            self._send_json({
                "ok": True,
                "item": actividad
            }, status=201)
            return

        if path == "/api/resultados":
            modulo = self._get_modulo()
            if modulo is None:
                return

            data = self._read_json_body()
            codigo = (data.get("codigo") or "").strip()
            nombre = (data.get("nombre") or "").strip()
            peso = data.get("peso") or 0

            error = self._validar_resultado(codigo, nombre, peso)
            if error:
                self._send_json({"ok": False, "error": error}, status=400)
                return

            try:
                resultado = create_resultado(modulo, codigo, nombre, peso)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "Ya existe un resultado con ese código"
                }, status=400)
                return

            self._send_json({
                "ok": True,
                "item": resultado
            }, status=201)
            return

        if path == "/api/indicadores":
            modulo = self._get_modulo()
            if modulo is None:
                return

            data = self._read_json_body()
            codigo = (data.get("codigo") or "").strip()
            nombre = (data.get("nombre") or "").strip()
            resultados = self._read_resultados_con_peso(data.get("resultados"))

            error = self._validar_indicador(modulo, codigo, nombre, resultados)
            if error:
                self._send_json({"ok": False, "error": error}, status=400)
                return

            try:
                indicador = create_indicador(modulo, codigo, nombre, resultados)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se pudo crear el indicador. Revisa el código y las asociaciones con resultados"
                }, status=400)
                return

            self._send_json({
                "ok": True,
                "item": indicador
            }, status=201)
            return

        self._send_json({
            "ok": False,
            "error": "Ruta no encontrada"
        }, status=404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        modulo = self._get_modulo()
        if modulo is None:
            return

        if path.startswith("/api/estudiantes/"):
            estudiante_id = self._extract_id(path, "/api/estudiantes/")
            if estudiante_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return

            data = self._read_json_body()
            estudiante = data.get('estudiante') or ""
            if not estudiante:
                self._send_json({
                    "ok": False,
                    "error": "No se ha recibido un estudiante válido."
                }, status=400)
                return

            nombre = (estudiante.get("nombre") or "").strip()

            if not nombre:
                self._send_json({
                    "ok": False,
                    "error": "El nombre es obligatorio"
                }, status=400)
                return

            try:
                estudiante = update_estudiante(modulo, estudiante_id, nombre)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "Ya existe un/a estudiante con ese nombre"
                }, status=400)
                return

            if estudiante is None:
                self._send_json({
                    "ok": False,
                    "error": "Estudiante no encontrado"
                }, status=404)
                return

            self._send_json({
                "ok": True,
                "item": estudiante
            })
            return

        if path.startswith("/api/actividades/"):
            actividad_id = self._extract_id(path, "/api/actividades/")
            if actividad_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return

            data = self._read_json_body()
            codigo = (data.get("codigo") or "").strip()
            nombre = (data.get("nombre") or "").strip()
            fecha_raw = (data.get("fecha") or "").strip()
            fecha = fecha_raw if fecha_raw else None
            indicadores = self._read_indicadores(data.get("indicadores"))

            error = self._validar_actividad(modulo, codigo, nombre, fecha, indicadores)
            if error:
                self._send_json({"ok": False, "error": error}, status=400)
                return

            try:
                actividad = update_actividad(modulo, actividad_id, codigo, nombre, fecha, indicadores)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se pudo actualizar la actividad. Revisa el código y las asociaciones con indicadores"
                }, status=400)
                return

            if actividad is None:
                self._send_json({
                    "ok": False,
                    "error": "Actividad no encontrada"
                }, status=404)
                return

            self._send_json({
                "ok": True,
                "item": actividad
            })
            return

        if path.startswith("/api/resultados/"):
            resultado_id = self._extract_id(path, "/api/resultados/")
            if resultado_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return
            
            data = self._read_json_body()
            resultado = data.get("resultado")
            if resultado is None:
                self._send_json({"ok": False, "error": "Objeto recibido inválido"}, status=400)
                return
            
            codigo = (resultado.get("codigo") or "").strip()
            nombre = (resultado.get("nombre") or "").strip()
            peso = resultado.get("peso") or 0

            error = self._validar_resultado(codigo, nombre, peso)
            if error:
                self._send_json({"ok": False, "error": error}, status=400)
                return

            try:
                resultado = update_resultado(modulo, resultado_id, codigo, nombre, peso)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "Ya existe un resultado con ese código"
                }, status=400)
                return

            if resultado is None:
                self._send_json({
                    "ok": False,
                    "error": "Resultado no encontrado"
                }, status=404)
                return

            self._send_json({
                "ok": True,
                "item": resultado
            })
            return

        if path.startswith("/api/indicadores/"):
            indicador_id = self._extract_id(path, "/api/indicadores/")
            if indicador_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return

            data = self._read_json_body()
            codigo = (data.get("codigo") or "").strip()
            nombre = (data.get("nombre") or "").strip()
            resultados = self._read_resultados_con_peso(data.get("resultados"))

            error = self._validar_indicador(modulo, codigo, nombre, resultados)
            if error:
                self._send_json({"ok": False, "error": error}, status=400)
                return

            try:
                indicador = update_indicador(modulo, indicador_id, codigo, nombre, resultados)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se pudo actualizar el indicador. Revisa el código y las asociaciones con resultados"
                }, status=400)
                return

            if indicador is None:
                self._send_json({
                    "ok": False,
                    "error": "Indicador no encontrado"
                }, status=404)
                return

            self._send_json({
                "ok": True,
                "item": indicador
            })
            return

        if path == "/api/calificaciones":
            data = self._read_json_body()

            actividad_id = self._read_optional_positive_int(data.get("actividad_id"))
            estudiante_id = self._read_optional_positive_int(data.get("estudiante_id"))
            items = self._read_calificacion_items(data.get("items"))
            error = self._validar_calificacion(modulo, actividad_id, estudiante_id, items)
            if error:
                self._send_json({"ok": False, "error": error}, status=400)
                return

            try:
                guardar_calificacion(modulo, actividad_id, estudiante_id, items)
            except ValueError as exc:
                self._send_json({"ok": False, "error": str(exc)}, status=400)
                return
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se pudo guardar la calificación"
                }, status=400)
                return

            self._send_json({"ok": True})
            return

        self._send_json({
            "ok": False,
            "error": "Ruta no encontrada"
        }, status=404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        modulo = self._get_modulo()
        if modulo is None:
            return

        if path.startswith("/api/estudiantes/"):
            estudiante_id = self._extract_id(path, "/api/estudiantes/")
            if estudiante_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return

            deleted = delete_estudiante(modulo, estudiante_id)
            if not deleted:
                self._send_json({
                    "ok": False,
                    "error": "Estudiante no encontrado"
                }, status=404)
                return

            self._send_json({"ok": True})
            return

        if path.startswith("/api/actividades/"):
            actividad_id = self._extract_id(path, "/api/actividades/")
            if actividad_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return

            try:
                deleted = delete_actividad(modulo, actividad_id)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se puede eliminar la actividad porque está siendo utilizada"
                }, status=400)
                return

            if not deleted:
                self._send_json({
                    "ok": False,
                    "error": "Actividad no encontrada"
                }, status=404)
                return

            self._send_json({"ok": True})
            return

        if path.startswith("/api/resultados/"):
            resultado_id = self._extract_id(path, "/api/resultados/")
            if resultado_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return

            try:
                deleted = delete_resultado(modulo, resultado_id)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se puede eliminar el resultado porque está siendo utilizado"
                }, status=400)
                return

            if not deleted:
                self._send_json({
                    "ok": False,
                    "error": "Resultado no encontrado"
                }, status=404)
                return

            self._send_json({"ok": True})
            return

        if path.startswith("/api/indicadores/"):
            indicador_id = self._extract_id(path, "/api/indicadores/")
            if indicador_id is None:
                self._send_json({"ok": False, "error": "ID inválido"}, status=400)
                return

            try:
                deleted = delete_indicador(modulo, indicador_id)
            except sqlite3.IntegrityError:
                self._send_json({
                    "ok": False,
                    "error": "No se puede eliminar el indicador porque está siendo utilizado"
                }, status=400)
                return

            if not deleted:
                self._send_json({
                    "ok": False,
                    "error": "Indicador no encontrado"
                }, status=404)
                return

            self._send_json({"ok": True})
            return

        if path == "/api/calificaciones":
            params = parse_qs(parsed.query)

            actividad_id = self._read_optional_positive_int(params.get("actividad_id"))
            estudiante_id = self._read_optional_positive_int(params.get("estudiante_id"))

            if actividad_id is None or estudiante_id is None:
                self._send_json({
                    "ok": False,
                    "error": "Debes indicar una actividad y un estudiante válidos"
                }, status=400)
                return

            deleted = borrar_calificacion(modulo, actividad_id, estudiante_id)

            self._send_json({
                "ok": True,
                "deleted": deleted
            })
            return

        self._send_json({
            "ok": False,
            "error": "Ruta no encontrada"
        }, status=404)

    def _read_json_body(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def _extract_id(self, path: str, prefix: str) -> int | None:
        raw = path.removeprefix(prefix).strip("/")
        if not raw.isdigit():
            return None
        return int(raw)

    def _validar_resultado(self, codigo: str, nombre: str, peso: int) -> str | None:
        if not codigo:
            return "El código es obligatorio"
        if not nombre:
            return "El nombre es obligatorio"
        if not peso:
            return "El peso es obligatorio"

        try:
            peso_num = int(peso)
            if peso_num <= 0:
                return "El peso debe ser mayor que 0"
        except ValueError:
            return "El peso debe ser un número entero"

        return None

    def _read_int_list(self, value) -> list[int] | None:
        if value is None:
            return []

        if not isinstance(value, list):
            return None

        ids = []

        for item in value:
            if isinstance(item, bool):
                return None

            try:
                numero = int(item)
            except (TypeError, ValueError):
                return None

            if numero <= 0:
                return None

            if numero not in ids:
                ids.append(numero)

        return ids

    def _read_resultados_con_peso(self, value) -> list[dict] | None:
        if value is None:
            return []

        if not isinstance(value, list):
            return None

        resultados = []
        ids_vistos = set()

        for item in value:
            if not isinstance(item, dict):
                return None

            id_resultado = item.get("id_resultado")
            peso = item.get("peso")

            if isinstance(id_resultado, bool) or isinstance(peso, bool):
                return None

            try:
                id_resultado = int(id_resultado)
                peso = int(peso)
            except (TypeError, ValueError):
                return None

            if id_resultado <= 0 or peso <= 0:
                return None

            if id_resultado in ids_vistos:
                return None

            ids_vistos.add(id_resultado)
            resultados.append({
                "id_resultado": id_resultado,
                "peso": peso,
            })

        return resultados

    def _validar_indicador(self, modulo: str, codigo: str, nombre: str, resultados: list[dict] | None) -> str | None:
        if not codigo:
            return "El código es obligatorio"

        if not nombre:
            return "El nombre es obligatorio"

        if resultados is None:
            return "Las asociaciones resultado/peso no son válidas"

        resultados_existentes = {item["id"] for item in list_resultados(modulo)}

        for item in resultados:
            if item["id_resultado"] not in resultados_existentes:
                return "Alguno de los resultados seleccionados no existe"

            if item["peso"] <= 0:
                return "Todos los pesos deben ser mayores que 0"

        return None

    def _read_indicadores(self, value) -> list[dict] | None:
        if value is None:
            return []

        if not isinstance(value, list):
            return None

        indicadores = []
        ids_vistos = set()

        for item in value:
            if not isinstance(item, dict):
                return None

            id_indicador = item.get("id_indicador")

            if isinstance(id_indicador, bool):
                return None

            try:
                id_indicador = int(id_indicador)
            except (TypeError, ValueError):
                return None

            if id_indicador <= 0:
                return None

            if id_indicador in ids_vistos:
                return None

            tipo_calificacion = item.get("tipo_calificacion", "ponderada")
            if tipo_calificacion not in ("ponderada", "maxima", "minima"):
                return None

            peso = item.get("peso")
            if peso is not None:
                if isinstance(peso, bool):
                    return None
                try:
                    peso = int(peso)
                except (TypeError, ValueError):
                    return None
                if peso < 0:
                    return None

            ids_vistos.add(id_indicador)
            indicadores.append({
                "id_indicador": id_indicador,
                "tipo_calificacion": tipo_calificacion,
                "peso": peso,
            })

        return indicadores

    def _validar_actividad(self, modulo: str, codigo: str, nombre: str, fecha: str | None, indicadores: list[dict] | None) -> str | None:
        if not codigo:
            return "El código es obligatorio"

        if not nombre:
            return "El nombre es obligatorio"

        if fecha is not None:
            try:
                date.fromisoformat(fecha)
            except ValueError:
                return "La fecha debe tener formato YYYY-MM-DD y ser válida"

        if indicadores is None:
            return "Las asociaciones de indicadores no son válidas"

        indicadores_existentes = {item["id"] for item in list_indicadores(modulo)}
        for item in indicadores:
            if item["id_indicador"] not in indicadores_existentes:
                return "Alguno de los indicadores seleccionados no existe"

        return None

    def _read_optional_positive_int(self, value) -> int | None:
        if value in (None, "", []):
            return None

        if isinstance(value, list):
            if not value:
                return None
            value = value[0]

        if isinstance(value, bool):
            return None

        try:
            numero = int(value)
        except (TypeError, ValueError):
            return None

        if numero <= 0:
            return None

        return numero

    def _read_calificacion_items(self, value) -> list[dict] | None:
        if value is None:
            return []

        if not isinstance(value, list):
            return None

        ids_vistos = set()
        items = []

        for item in value:
            if not isinstance(item, dict):
                return None

            id_indicador = item.get("id_indicador")
            nivel_logro = item.get("nivel_logro")
            incremento = item.get("incremento")

            if isinstance(id_indicador, bool):
                return None

            try:
                id_indicador = int(id_indicador)
            except (TypeError, ValueError):
                return None

            if id_indicador <= 0 or id_indicador in ids_vistos:
                return None

            ids_vistos.add(id_indicador)

            if nivel_logro in (None, ""):
                nivel = None
            else:
                if isinstance(nivel_logro, bool):
                    return None
                try:
                    nivel = int(nivel_logro)
                except (TypeError, ValueError):
                    return None

                if nivel < 0 or nivel > 10:
                    return None

            if incremento in (None, ""):
                incremento = None
            else:
                try:
                    float(incremento)
                except (TypeError, ValueError):
                    return None

            items.append({
                "id_indicador": id_indicador,
                "nivel_logro": nivel,
                "incremento": incremento,
            })

        return items

    def _validar_calificacion(self, modulo: str, actividad_id: int | None, estudiante_id: int | None, items: list[dict] | None) -> str | None:
        if actividad_id is None:
            return "Debes seleccionar una actividad"

        if estudiante_id is None:
            return "Debes seleccionar un/a estudiante"

        if items is None:
            return "Los datos de la evaluación no son válidos"

        actividades_validas = {item["id"] for item in list_actividades(modulo)}
        if actividad_id not in actividades_validas:
            return "La actividad seleccionada no existe"

        estudiantes_validos = {item["id"] for item in list_estudiantes(modulo)}
        if estudiante_id not in estudiantes_validos:
            return "La/el estudiante seleccionado no existe"

        for item in items:
            nivel = item["nivel_logro"]
            if nivel is not None and (nivel < 0 or nivel > 10):
                return "Alguno de los niveles de logro no es válido"

        return None

    def _send_json(self, data: dict, status: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _get_modulo(self) -> str | None:
        raw = (self.headers.get("X-CCXI-Modulo") or "").strip()

        try:
            modulo = normalize_modulo(raw)
        except ValueError as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=400)
            return None
        if modulo not in list_valid_modulos():
            self._send_json({
                "ok": False,
                "error": "El módulo seleccionado no existe o no es válido (" + modulo + ")"
            }, status=400)
            return None

        return modulo


def main() -> None:
    ensure_data_dir()
    server = ThreadingHTTPServer((HOST, PORT), CCXIHandler)
    print(f"ccxi disponible en http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
