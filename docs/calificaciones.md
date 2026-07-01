# Sistema de Calificación — ccxi

## Datos básicos

Cada calificación se compone de:

- **`nivel_logro`** (entero 0–10): nota del indicador en una actividad concreta
- **`incremento`** (real): ajuste (+/-) que se suma al cálculo final

## Tipos de calificación (`Indicador_Actividad.tipo_calificacion`)

Al asociar un indicador a una actividad se elige un tipo que determina cómo se agrega esa nota:

| Tipo | Peso | Significado |
|------|------|-------------|
| `ponderada` | Entero ≥ 0 (nullable) | La nota se promedia ponderadamente con otras del mismo tipo. Si peso es `null` se trata como 1. |
| `maxima` | Siempre `null` | Se toma el valor máximo entre todas las actividades de este tipo. |
| `minima` | Siempre `null` | Se toma el valor mínimo entre todas las actividades de este tipo. |

## Cálculo de la calificación actual

Para un estudiante e indicador dados, se recogen **todas** las `Calificacion` registradas en cualquier actividad y se agrupan por `tipo_calificacion`.

### Regla 1 — Solo ponderadas (no hay máxima ni mínima)

```
calificación = media_ponderada(nivel_logro, peso) + Σ incrementos
```

### Regla 2 — Hay alguna máxima (no hay mínima)

```
calificación = min( max(nivel_logro_máximas), media_ponderada(nivel_logro_ponderadas) ) + Σ incrementos
```

Si no hay ponderadas, se omite la media y queda `max(máximas) + incrementos`.

### Regla 3 — Hay alguna mínima (prevalece sobre cualquier otra)

```
calificación = max(nivel_logro_mínimas)
```

No se suman incrementos. Esta regla tiene prioridad absoluta: una sola actividad de tipo `minima` anula el resto de tipos.

## Flujo de trabajo

1. **Crear actividad** → asociar indicadores con tipo y peso
2. **Ir a Calificaciones** → seleccionar actividad y estudiante
3. Para cada indicador:
   - Si está **asociado** a la actividad: se muestran campos `nivel_logro` (0–10) e `incremento`
   - Si **no está asociado**: solo `incremento` (no tiene `nivel_logro` porque no pertenece a la actividad)
4. Pulsar **Guardar calificaciones** → se persisten los valores de la actividad actual
5. La columna **Calificación actual** muestra el resultado de aplicar las reglas 1–3 sobre el histórico completo del estudiante en ese indicador

## Esquema BD relevante

```sql
CREATE TABLE "Calificacion" (
    "id_estudiante" INTEGER NOT NULL,
    "id_indicador"  INTEGER NOT NULL,
    "id_actividad"  INTEGER NOT NULL,
    "nivel_logro"   INTEGER,
    "incremento"    REAL,
    PRIMARY KEY ("id_estudiante", "id_indicador", "id_actividad")
);

CREATE TABLE "Indicador_Actividad" (
    "id_indicador"      INTEGER NOT NULL,
    "id_actividad"      INTEGER NOT NULL,
    "tipo_calificacion" TEXT NOT NULL DEFAULT 'ponderada'
        CHECK (tipo_calificacion IN ('ponderada', 'maxima', 'minima')),
    "peso"              INTEGER CHECK (peso >= 0),
    PRIMARY KEY ("id_indicador", "id_actividad")
);
```
