[← Volver al índice](indice.md)

# Gestión de Calificaciones — ccxi

## 10.1 Acceso

Ve a la pestaña **Calificaciones**. Se muestran dos desplegables: **Actividad** y **Estudiante**. Al seleccionar ambos, se carga la tabla con los indicadores que se pueden calificar.

El botón **Guardar calificaciones** solo aparece cuando hay una actividad y un estudiante seleccionados.

## 10.2 Interfaz de calificación

La tabla muestra cuatro columnas:

| Columna | Descripción |
|---------|-------------|
| **Indicador** | Código y nombre del indicador |
| **Calificación actual** | Nota resultante de aplicar las reglas de agregación sobre el histórico completo del estudiante en ese indicador |
| **Nivel de logro (0-10)** | Nota del indicador en esta actividad (solo para indicadores asociados a la actividad) |
| **Incremento (+/-)** | Ajuste decimal que se suma al cálculo final |

Si un indicador **no está asociado** a la actividad, solo muestra la columna de Incremento (no tiene nivel de logro porque no pertenece a la actividad).

## 10.3 Calificar

1. Selecciona una **actividad** y un **estudiante**
2. Para cada indicador asociado, introduce:
   - **Nivel de logro**: número entero entre 0 y 10
   - **Incremento**: valor decimal positivo o negativo (opcional)
3. Para indicadores no asociados que aparezcan en la tabla (porque ya tenían calificación previa), solo puedes añadir un incremento
4. Pulsa **Guardar calificaciones**

Al guardar se reemplazan todas las calificaciones de esa actividad y estudiante por los valores actuales.

## 10.4 Añadir indicadores extra

En el pie de la tabla puedes añadir indicadores que no están asociados originalmente a la actividad:

1. Escribe al menos 3 caracteres en el buscador para encontrar indicadores
2. Selecciona un indicador de las sugerencias
3. Asigna un incremento (opcional)
4. Pulsa **Añadir**

Esto permite registrar mejoras o penalizaciones en indicadores que no forman parte de la actividad. El incremento se aplicará solo a este estudiante.

## 10.5 Tipos de calificación

Al crear una actividad, cada indicador asociado recibe un tipo que determina cómo se agrega su nota:

| Tipo | Peso | Comportamiento |
|------|------|---------------|
| **Ponderada** | Opcional (entero ≥ 0) | La nota se promedia ponderadamente con otras actividades del mismo tipo. Si no se asigna peso, se trata como 1. |
| **Máxima** | No aplica | Se toma el valor máximo alcanzado entre todas las actividades de este tipo. |
| **Mínima** | No aplica | Prevalece sobre cualquier otro tipo. Una sola actividad de tipo mínima determina la calificación final del indicador y no se suman incrementos. |

## 10.6 Cálculo de la calificación actual

Para cada indicador, la calificación actual se calcula sobre **todas** las calificaciones registradas del estudiante en cualquier actividad, agrupadas por tipo:

1. **Solo ponderadas**: media ponderada de las notas (según el peso de cada actividad) más la suma de todos los incrementos.
2. **Hay alguna máxima (sin mínimas)**: se toma el valor máximo de las actividades tipo máxima, y se combina con la media ponderada (si existe), quedándose con el menor de ambos valores. Se suman los incrementos.
3. **Hay alguna mínima**: se toma el valor máximo de las actividades tipo mínima. Esta nota prevalece sobre cualquier otro tipo y no se suman incrementos.

## 10.7 Borrar calificaciones

Para borrar todas las calificaciones de una actividad y estudiante:

1. Selecciona la actividad y el estudiante
2. Vacía los campos de nivel de logro e incremento de todos los indicadores
3. Pulsa **Guardar calificaciones**

También puedes eliminar filas de indicadores extra pulsando el botón **Eliminar** antes de guardar.

## 10.8 Cambio de módulo

Al seleccionar otro módulo en el panel superior, los selectores de actividad y estudiante se recargan automáticamente. También se actualizan al crear, editar o eliminar actividades o estudiantes.

## 10.9 Observaciones

- El **nivel de logro** debe ser un número entero entre 0 y 10
- El **incremento** puede ser cualquier número decimal, positivo o negativo
- La **calificación actual** se actualiza cada vez que guardas, reflejando el histórico completo del estudiante
- Para consultar el desglose detallado de cómo se calcula cada calificación, usa los [informes](11_informes.md)
