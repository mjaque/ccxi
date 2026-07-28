# ccxi — Calificador de Competencias por Indicadores

Aplicación web para la calificación de competencias por indicadores, adecuada para ciclos de Formación Profesional. 
Permite gestionar módulos, estudiantes, resultados de aprendizaje, indicadores de logro, actividades evaluables y calificaciones, al tiempo que elabora informes de grupo y de estudiante.

## Stack

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3, `http.server` (REST API nativa) |
| Base de datos | SQLite (`.sqlite` independiente por módulo) |
| Frontend | Vanilla JS (ES modules) sin frameworks |
| CSS | Reset + app.css + ccxi.css |

## Funcionalidades

- Gestión de módulos (creación y selección de bases de datos independientes)
- CRUD de estudiantes
- Definición de resultados de aprendizaje con pesos
- Definición de indicadores de logro asociados a resultados
- Búsqueda de indicadores
- Creación de actividades evaluables con indicadores asociados y tipo de calificación (ponderada, máxima, mínima)
- Calificación de estudiantes por actividad con nivel de logro (0-10) e incremento
- Cálculo automático de nota actual por indicador
- Informe detallado de estudiante
- Informe de actividades agrupadas por resultados de aprendizaje
- Informes de grupo con cuartiles (Q1, Q2, Q3) por resultados e indicadores
- Informe de grupo de actividades por resultados con cuartiles (Q1, Q2, Q3) 

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (SPA)                           │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  App     │  │ Controladores│  │  Modelos             │   │
│  │(orquest.)│──│ (MVC)        │──│ (Estudiante,         │   │
│  │          │  │              │  │  Resultado,Indicador)│   │
│  └──────────┘  └──────────────┘  └──────────────────────┘   │
│                       │                                     │
│              ┌────────┴────────┐                            │
│              │ API (Singleton) │── BusEventos (pub/sub)     │
│              └────────┬────────┘                            │
└───────────────────────┼─────────────────────────────────────┘
                        │ HTTP (REST JSON)
┌───────────────────────┼─────────────────────────────────────┐
│              ┌────────┴────────┐        Backend             │
│              │  CCXIHandler    │                            │
│              │ (http.server)   │                            │
│              └────────┬────────┘                            │
│                       │                                     │
│              ┌────────┴────────┐                            │
│              │  Repositories   │                            │
│              │ (SQL)           │                            │
│              └────────┬────────┘                            │
│                       │                                     │
│              ┌────────┴────────┐                            │
│              │  SQLite(.sqlite)│                            │
│              └─────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### Backend (REST + Repository)

Servidor HTTP nativo (`http.server.ThreadingHTTPServer`) con enrutamiento manual. Cada endpoint delega en funciones de `repositories/` que reciben el nombre del módulo activo (header `X-CCXI-Modulo`). Las respuestas siguen el formato `{"ok": bool, ...}`.

### Frontend (SPA con MVC + EventBus)

- **App** orquesta la aplicación: crea controladores, gestiona cambio de vistas
- **Controladores** extienden una clase base que proporciona carga dinámica de vistas HTML, helpers de UI y acceso a API/EventBus
- **API** (singleton) envía peticiones REST con inyección automática del header de módulo
- **BusEventos** (pub/sub vía `EventTarget`) desacopla controladores mediante eventos (`cambioModulo`, `cambioEstudiante`, etc.)
- **Modelos** de dominio con serialización

### Base de datos

Una base de datos SQLite por módulo en `data/`. Ocho tablas: `Metadatos`, `Estudiante`, `Resultado`, `Indicador`, `Actividad`, `Indicador_Resultado`, `Indicador_Actividad`, `Calificacion`. Claves foráneas con `ON DELETE CASCADE`.

## Estructura del proyecto

```
ccxi/
├── backend/
│   ├── app.py                 # Servidor HTTP + rutas REST
│   ├── db.py                  # Gestión de conexiones SQLite
│   ├── schema.sql             # Esquema SQL (8 tablas)
│   ├── repositories/          # Capa de acceso a datos
│   │   ├── estudiantes.py
│   │   ├── actividades.py
│   │   ├── resultados.py
│   │   ├── indicadores.py
│   │   ├── calificaciones.py
│   │   └── informes.py
│   ├── controladores/         # Legacy (server-side XML)
│   └── vistas/                # Legacy (plantillas XML)
├── frontend/
│   ├── html/                  # Vistas HTML parciales
│   ├── js/
│   │   ├── app.js             # Punto de entrada SPA
│   │   ├── controladores/     # Controladores frontend
│   │   ├── modelos/           # Modelos de dominio
│   │   └── servicios/         # API client, EventBus
│   └── css/
├── data/                      # Bases de datos SQLite
├── tests/                     # Tests Python + dataset
├── docs/                      # Documentación
├── scripts/                   # Utilidades
├── backups/                   # Copias de seguridad
├── LICENSE                    # GPL v3
└── package.json
```

## API REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Estado del servidor |
| GET | `/api/modulos` | Lista módulos |
| POST | `/api/modulos` | Crear módulo |
| GET | `/api/estudiantes` | Lista estudiantes |
| POST | `/api/estudiantes` | Crear estudiante |
| PUT | `/api/estudiantes/{id}` | Actualizar estudiante |
| DELETE | `/api/estudiantes/{id}` | Eliminar estudiante |
| GET | `/api/actividades` | Lista actividades |
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
| GET | `/api/calificaciones/contexto` | Contexto para calificar |
| PUT | `/api/calificaciones` | Guardar calificación |
| DELETE | `/api/calificaciones` | Borrar calificación |
| GET | `/api/informes/estudiantes` | Informe de estudiante |
| GET | `/api/informes/actividades-por-resultados` | Informe por resultados |
| GET | `/api/informes/grupo` | Informe de grupo con cuartiles |
| GET | `/api/informes/actividades-por-resultados-grupo` | Informe de grupo por actividades con cuartiles |
| GET | `/api/informes/indicadores` | Listado de indicadores agrupados por resultado |

## Patrones de diseño

| Patrón | Dónde |
|--------|-------|
| Repository | `backend/repositories/` — cada archivo encapsula SQL de una entidad |
| Controller (MVC) | `frontend/js/controladores/` — gestionan UI y eventos |
| Singleton | `frontend/js/servicios/api.js` — instancia única del cliente HTTP |
| Pub/Sub | `frontend/js/servicios/bus_eventos.js` — desacopla controladores |
| Template Method | `Controlador` base — define ciclo de vida que las subclases implementan |
| Front Controller | `frontend/js/app.js` — centraliza creación de controladores |

## Requisitos

- Python 3.8+
- Navegador web moderno (Chrome, Firefox, Edge)

## Inicio rápido

```bash
git clone <repo>
cd ccxi
python3 backend/app.py
```

Abrir `http://127.0.0.1:8000` en el navegador.

## Tests (incompletos)

```bash
npm test
```

Incluye un dataset de prueba (`tests/dataset1.sql`) con 10 estudiantes, 5 resultados de aprendizaje, 25 indicadores y 5 actividades.

## Licencia

GNU General Public License v3.0. Ver [LICENSE](LICENSE).
