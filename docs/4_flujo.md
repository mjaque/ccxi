[← Volver al índice](indice.md)

## 4. Flujo de trabajo recomendado

El orden lógico para usar CCxI es el siguiente. Puedes saltarte pasos o volver atrás cuando quieras: cada sección es independiente.

```
  1. Módulo    →  2. Estudiantes  →  3. RA  →  4. Indicadores  →  5. Actividades  →  6. Calificar  →  7. Informes
```

### 4.1 Paso 1 — Crear o seleccionar un módulo/grupo

Desde el panel superior, siempre visible, elige un módulo existente del desplegable o escribe un nombre nuevo y pulsa **Crear**.

Cada módulo es un archivo `.sqlite` independiente en `data/`, así que puedes tener todos los cursos y grupos que necesites sin que se mezclen ([más info](3_conceptos.md#31-m%C3%B3dulogrupo)).

### 4.2 Paso 2 — Dar de alta los estudiantes

Ve a la pestaña **Estudiantes**. Escribe el nombre y pulsa **Guardar**. Puedes editar o eliminar estudiantes desde la tabla.

No hace falta que los metas todos de golpe: puedes ir añadiendo sobre la marcha.

### 4.3 Paso 3 — Definir los Resultados de Aprendizaje

Ve a la pestaña **Resultados**. Crea cada RA con:
- **Código** (ej. RA01, RA02…)
- **Nombre** (tal cual aparece en tu programación)
- **Peso** (importancia relativa respecto al total del módulo)

Pulsa **Guardar** y el RA aparece en la tabla. Puedes editarlo o borrarlo después.

Los RA son la columna vertebral de la evaluación: todo lo demás cuelga de ellos ([más info](3_conceptos.md#32-resultado-de-aprendizaje)).

### 4.4 Paso 4 — Crear los Indicadores de Logro

Ve a la pestaña **Indicadores**. Cada indicador necesita:
- **Código** (ej. IL1.a, IL2.c.3…)
- **Nombre** descriptivo
- **Asociación a uno o varios RA**, con un peso en cada relación

Selecciona un RA del desplegable, asigna el peso, pulsa **Añadir** y repite para cada RA al que pertenezca el indicador. Después pulsa **Guardar**.

Los indicadores son los criterios medibles que te permiten saber si un estudiante ha alcanzado cada RA ([más info](3_conceptos.md#33-indicador-de-logro)).

### 4.5 Paso 5 — Crear las Actividades Evaluables

Ve a la pestaña **Actividades**. Cada actividad necesita:
- **Código** (ej. AE1.1, EX2, TRAB3…)
- **Nombre**
- **Fecha** (opcional)
- **Asociación a uno o varios indicadores**, cada uno con un **tipo de calificación** (ponderada, máxima o mínima) y opcionalmente un **peso**

Usa el buscador para encontrar indicadores y añadirlos a la actividad. Después pulsa **Guardar**.

Puedes crear tantas actividades como necesites: exámenes, trabajos, prácticas, ejercicios… ([más info](3_conceptos.md#34-actividad-evaluable)).

### 4.6 Paso 6 — Calificar

Ve a la pestaña **Calificaciones**. Selecciona una **actividad** y un **estudiante**. El sistema te muestra una tabla con todos los indicadores asociados a esa actividad.

Para cada indicador puedes introducir:
- **Nivel de logro** (0-10)
- **Incremento** (valor decimal positivo o negativo, opcional)

También puedes añadir indicadores extra no asociados originalmente a la actividad para registrar incrementos adicionales.

Pulsa **Guardar calificaciones** para persistir. La columna *Calificación actual* muestra la nota resultante de aplicar las reglas de agregación sobre el histórico completo ([más info](10_calificaciones.md)).

### 4.7 Paso 7 — Generar informes

Ve a la pestaña **Informes**. Hay cuatro tipos:

| Informe | Para qué sirve |
|---------|---------------|
| **Informe de Estudiante** | Calificación del estudiante en cada RA, con detalle por IL |
| **Informe de Actividades por Resultados** | Misma información que el anterior, pero desglosada por actividades |
| **Informe de Grupo** | Distribución del grupo en cuartiles (Q1, Q2, Q3) para cada RA e IL |
| **Informe de Actividades por Resultados (Grupo)** | Cuartiles por actividad, agrupados por RA; orientado al profesor |

Todos los informes aceptan una **fecha de corte** opcional para generar informes parciales (por ejemplo, solo hasta la primera evaluación) y se abren en una pestaña nueva ([más info](3_conceptos.md#37-informes-de-estudiante)).

### 4.8 Consejos prácticos

- **El orden no es rígido.** Puedes crear los RA antes de dar de alta estudiantes, o crear actividades antes de terminar todos los indicadores. El sistema no te lo impedirá.
- **No tienes que calificar todo de una vez.** Puedes calificar una actividad para unos pocos estudiantes, cambiar a otra actividad y volver después.
- **Si cambias de módulo** en el desplegable superior, todos los datos de las pestañas se recargan automáticamente para el módulo seleccionado.