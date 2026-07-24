# ccxi — Calificador de Competencias por Indicadores

## Descripción

Aplicación web educativa para evaluación por competencias. Permite gestionar módulos, estudiantes, resultados de aprendizaje, indicadores de logro, actividades evaluables, calificaciones e informes de grupo/estudiante.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3, `http.server` (REST API nativa) |
| Base de datos | SQLite (`.sqlite` independiente por módulo) |
| Frontend | Vanilla JS (ES modules), sin frameworks |
| CSS | Reset + app.css + ccxi.css |
| Estilo | Python: `snake_case` / JS: `camelCase` (clases PascalCase) |

## Estructura

```
ccxi/
├── backend/
│   ├── app.py                 # Servidor HTTP + rutas REST (endpoints en GET/POST/PUT/DELETE)
│   ├── db.py                  # Gestión de conexiones SQLite, creación/validación de módulos
│   ├── schema.sql             # Esquema SQL (8 tablas)
│   ├── controladores/         # (legacy) Controladores server-side con minidom/XML
│   ├── repositories/          # Capa de acceso a datos (consultas SQL)
│   │   ├── estudiantes.py     # CRUD estudiantes
│   │   ├── actividades.py     # CRUD actividades
│   │   ├── resultados.py      # CRUD resultados de aprendizaje
│   │   ├── indicadores.py     # CRUD indicadores de logro
│   │   ├── calificaciones.py  # CRUD calificaciones
│   │   └── informes.py        # Informes de estudiante y grupo
│   ├── vistas/                # (legacy) Plantillas XML (.xml.borrar)
│   ├── servicios/             # (vacío) Capa de negocio prevista
│   └── informes/              # (vacío)
├── frontend/
│   ├── html/                  # Vistas HTML parciales (cargadas dinámicamente)
│   │   ├── index.html         # Shell de la SPA
│   │   ├── modulos.html
│   │   ├── estudiantes.html
│   │   ├── resultados.html
│   │   ├── indicadores.html
│   │   ├── actividades.html
│   │   ├── calificaciones.html
│   │   └── informes.html
│   ├── js/
│   │   ├── app.js             # Punto de entrada SPA
│   │   ├── controladores/     # Controladores frontend (MVC)
│   │   │   ├── controlador.js # Clase base Controlador
│   │   │   ├── estado.js     # Health check inicial
│   │   │   ├── modulos.js    # Selector/creación de módulos
│   │   │   ├── estudiantes.js
│   │   │   ├── resultados.js
│   │   │   ├── indicadores.js
│   │   │   ├── actividades.js
│   │   │   ├── calificaciones.js
│   │   │   └── informes.js   # Informes en nueva pestaña
│   │   ├── modelos/           # Modelos de dominio
│   │   │   ├── estudiante.js
│   │   │   ├── resultado.js
│   │   │   └── indicador.js
│   │   └── servicios/         # API client, EventBus
│   │       ├── api.js         # Cliente HTTP singleton
│   │       └── bus_eventos.js # Pub/sub EventTarget
│   ├── css/
│   │   ├── reset.css
│   │   ├── app.css
│   │   └── ccxi.css
│   └── favicon.svg
├── data/                      # Bases de datos SQLite (una por módulo)
├── tests/
│   └── dataset1.sql           # Dataset de prueba (10 estudiantes, 5 RA, 25 indicadores, 5 actividades)
├── scripts/                   # Utilidades (análisis con Ollama, etc.)
├── backups/                   # Copias de seguridad de BD
├── docs/
│   └── calificaciones.md      # Documentación del sistema de calificación
├── .gitignore
├── start-linux.sh             # Lanzador: python3 backend/app.py
└── start-win.bat              # Lanzador Windows: py -3 backend/app.py
```

## Arquitectura

### Frontend (SPA con MVC + EventBus)
- `App` (app.js) orquestra la aplicación: carga cada `Controlador` en su `<div>` correspondiente
- Los `Controlador` extienden `Controlador` base que proporciona: `api` (cliente REST), `div` (contenedor), `cargarVista()`, `mostrarError/informacion()`
- `BusEventos` (pub/sub vía `EventTarget`) desacopla controladores: `Controlador.busEventos.on('cambioModulo', ...)`
- `API` (singleton) envía peticiones REST con header `X-CCXI-Modulo`
- Las vistas HTML se cargan dinámicamente via `fetch()` en `cargarVista()`

### Backend (REST + Repository)
- `CCXIHandler` extiende `SimpleHTTPRequestHandler` y define `do_GET/POST/PUT/DELETE`
- Cada endpoint delega en funciones de `repositories/` que reciben `modulo` (nombre del .sqlite)
- Módulo activo se pasa por header HTTP `X-CCXI-Modulo`
- No hay autenticación (uso local)

### Base de datos
- Una base de datos `.sqlite` por módulo (curso/asignatura)
- Tablas: `Metadatos`, `Estudiante`, `Resultado`, `Indicador`, `Actividad`, `Indicador_Resultado`, `Indicador_Actividad`, `Calificacion`
- Niveles de logro permitidos: `0` a `10`

## API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servidor |
| GET | `/api/modulos` | Lista bases de datos |
| POST | `/api/modulos` | Crear módulo |
| GET | `/api/estudiantes` | Lista estudiante |
| POST | `/api/estudiantes` | Crear estudiante |
| PUT | `/api/estudiantes/{id}` | Actualizar estudiante |
| DELETE | `/api/estudiantes/{id}` | Eliminar estudiante |
| GET | `/api/actividades` | Lista actividad |
| POST | `/api/actividades` | Crear actividad (con indicadores) |
| PUT | `/api/actividades/{id}` | Actualizar actividad |
| DELETE | `/api/actividades/{id}` | Eliminar actividad |
| GET | `/api/resultados` | Lista resultados |
| POST | `/api/resultados` | Crear resultado |
| PUT | `/api/resultados/{id}` | Actualizar resultado |
| DELETE | `/api/resultados/{id}` | Eliminar resultado |
| GET | `/api/indicadores` | Lista indicadores |
| GET | `/api/indicadores/buscar?q=` | Buscar indicadores |
| POST | `/api/indicadores` | Crear indicador (con resultados+peso) |
| PUT | `/api/indicadores/{id}` | Actualizar indicador |
| DELETE | `/api/indicadores/{id}` | Eliminar indicador |
| GET | `/api/calificaciones/contexto?actividad_id=&estudiante_id=` | Contexto para calificar |
| PUT | `/api/calificaciones` | Guardar calificación |
| DELETE | `/api/calificaciones?actividad_id=&estudiante_id=` | Borrar calificación |
| GET | `/api/informes/estudiantes?estudiante_id=&fecha_informe=` | Informe de estudiante |
| GET | `/api/informes/grupo?fecha_informe=` | Informe de grupo |

## Comandos

```bash
python3 backend/app.py          # Arrancar servidor (http://127.0.0.1:8000)
npm run lint                    # Lint JS frontend (ESLint)
npm run lint:fix                # Lint + auto-corregir
npm test                        # Tests Python (unittest + discover)
```

## Convenciones de código

- **JS:** ES modules, clases con campos privados (`#campo`), `async/await`, snake_case para nombres de métodos privados
- **Python:** type hints, snake_case, docstrings en español
- **UI:** español, atributos HTML sin comillas donde posible (`lang=es`, `id=divEstado`)
- **Importaciones:** relativas en frontend, absolutas desde `backend/` en Python
- **Rutas API:** siempre devuelven `{"ok": bool, ...}` con código HTTP adecuado
- **BD:** nombres de tabla en doble comilla, parámetros con `?`, `PRAGMA foreign_keys = ON`

## Patrones

| Patrón | Dónde |
|--------|-------|
| Repository | `backend/repositories/` — cada archivo encapsula SQL de una entidad |
| Controller | Frontend: `controladores/*.js` gestionan UI y eventos |
| Singleton | `API` (`servicios/api.js`) — instancia única del cliente HTTP |
| Pub/Sub | `BusEventos` — desacopla controladores mediante eventos |
| MVC | Frontend: modelos (`modelos/`), vistas (`html/`), controladores (`controladores/`) |

## WIP / Notas

- Migración en curso de server-side XML/XSL → SPA con API REST
- `backend/controladores/` y `backend/vistas/` son legacy del viejo sistema con `minidom`
- `frontend/js/api.js` (raíz) es legacy — el nuevo cliente está en `frontend/js/servicios/api.js`
- `backend/repositories/informes.py` tiene funciones duplicadas (`_build_fecha_filter`, `_clamp_nota_indicador`, `_calcular_notas_indicadores`, `get_informe_alumnado`)
- `tests/` contiene `dataset1.sql` y tests Python (unittest con mock de BD)
- `backend/servicios/` y `backend/informes/` están vacíos
- TO DOs en: `modulos.js` (2 métodos sin implementar)
- `app.py` línea 9: import muerto de `ControladorPrincipal` (nunca se usa)
- No hay cliente frontend para `GET /api/informes/grupo` (solo existe el endpoint backend)
- No hay type checker configurado
