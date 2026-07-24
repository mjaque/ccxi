[← Volver al índice](indice.md)

# Gestión de Actividades Evaluables — ccxi

## 9.1 Acceso

Ve a la pestaña **Actividades**. Se muestra un formulario con los campos **Código**, **Nombre** y **Fecha**, un subbloque para **Asociar indicador** (buscador, tipo de calificación, peso), un buscador general y una tabla con el listado de actividades del módulo activo.

Cada fila de la tabla muestra el código, el nombre, la fecha y los indicadores asociados a la actividad.

## 9.2 Crear una actividad

1. Rellena los campos:
   - **Código** (obligatorio, no puede repetirse)
   - **Nombre** (obligatorio)
   - **Fecha** (opcional, formato AAAA-MM-DD)
2. En el subbloque **Asociar indicador**, añade los indicadores que evaluará esta actividad:
   - Escribe al menos 3 caracteres en el buscador para encontrar indicadores
   - Selecciona un indicador de las sugerencias que aparecen
   - Elige el **tipo de calificación** (ponderada, máxima o mínima)
   - Si el tipo es **ponderada**, puedes asignar un peso (opcional)
   - Pulsa **Añadir**
3. Repite para cada indicador que forme parte de la actividad
4. Pulsa **Guardar**

## 9.3 Tipos de calificación

| Tipo | Peso | Comportamiento |
|------|------|---------------|
| **Ponderada** | Opcional (entero ≥ 0) | La nota se promedia ponderadamente con otras actividades del mismo tipo. Si no se asigna peso, se trata como 1. |
| **Máxima** | No aplica | Se toma el valor máximo alcanzado entre todas las actividades de este tipo. |
| **Mínima** | No aplica | Prevalece sobre cualquier otro tipo. Una sola actividad de tipo mínima determina la calificación final del indicador. |

Para más detalle sobre cómo se combinan los tipos, consulta el [Sistema de Calificación](10_calificaciones.md).

## 9.4 Editar una actividad

1. Pulsa el botón **Editar** en la fila correspondiente de la tabla
2. Los datos y los indicadores asociados se cargan en el formulario
3. Modifica los campos o las asociaciones y pulsa **Guardar**

Para quitar un indicador asociado, pulsa el botón **Eliminar** en la fila correspondiente de la tabla de indicadores asociados.

## 9.5 Eliminar una actividad

1. Pulsa el botón **Eliminar** en la fila correspondiente
2. Se muestra un cuadro de confirmación
3. Confirma la eliminación

Al eliminar una actividad se borran también todas las calificaciones asociadas a ella. Esta operación no se puede deshacer.

## 9.6 Buscar actividades

El campo de búsqueda sobre la tabla filtra las actividades en tiempo real mientras escribes. Busca por código, nombre, fecha o indicador asociado.

## 9.7 Cambio de módulo

Al seleccionar otro módulo en el panel superior, la lista de actividades se recarga automáticamente. La lista también se actualiza cuando se crean, editan o eliminan indicadores en la pestaña de Indicadores.

## 9.8 Observaciones

- El **código** debe ser único dentro del módulo
- La **fecha** es opcional y se guarda en formato ISO (AAAA-MM-DD)
- Un mismo indicador no puede asociarse dos veces a la misma actividad
- El **peso** solo se aplica al tipo ponderada; para los tipos máxima y mínima se ignora
- Las actividades se ordenan por fecha descendente y luego alfabéticamente por código
- La pestaña de Calificaciones se actualiza automáticamente al crear, editar o eliminar actividades
