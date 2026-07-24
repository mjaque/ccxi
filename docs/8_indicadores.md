[← Volver al índice](indice.md)

# Gestión de Indicadores de Logro — ccxi

## 8.1 Acceso

Ve a la pestaña **Indicadores**. Se muestra un formulario con los campos **Código** y **Nombre**, un subbloque para **Asociar resultado**, un buscador y una tabla con el listado de indicadores del módulo activo.

Cada fila de la tabla muestra el código, el nombre y los resultados de aprendizaje asociados al indicador (con su peso entre paréntesis).

## 8.2 Crear un indicador

1. Rellena los campos:
   - **Código** (mínimo 3 caracteres, no puede repetirse)
   - **Nombre** (mínimo 3 caracteres)
2. En el subbloque **Asociar resultado**, selecciona un RA del desplegable, asigna un peso y pulsa **Añadir**
3. Repite para cada RA al que quieras asociar el indicador
4. Pulsa **Guardar**

Cada indicador debe estar asociado al menos a un resultado de aprendizaje.

## 8.3 Editar un indicador

1. Pulsa el botón **Editar** en la fila correspondiente de la tabla
2. Los datos se cargan en el formulario, incluyendo los RA asociados
3. Modifica los campos o las asociaciones y pulsa **Guardar**

Para quitar un RA asociado, pulsa el botón **Eliminar** en la fila correspondiente de la tabla de resultados asociados.

## 8.4 Eliminar un indicador

1. Pulsa el botón **Eliminar** en la fila correspondiente
2. Se muestra un cuadro de confirmación
3. Confirma la eliminación

Si el indicador tiene calificaciones registradas o está asociado a alguna actividad, el sistema impedirá la eliminación y mostrará un aviso. Elimina primero las actividades o calificaciones que dependan de él.

## 8.5 Buscar indicadores

El campo de búsqueda sobre la tabla filtra los indicadores en tiempo real mientras escribes. Busca por código, nombre o resultado de aprendizaje asociado. Si no hay coincidencias, la tabla muestra "No hay indicadores que coincidan con la búsqueda."

## 8.6 Cambio de módulo

Al seleccionar otro módulo en el panel superior, la lista de indicadores y el selector de RA se recargan automáticamente. La lista también se actualiza cuando se crean, editan o eliminan RA en la pestaña de Resultados.

## 8.7 Observaciones

- El **código** debe ser único dentro del módulo
- Cada indicador debe asociarse al menos a un RA; si no hay RA creados, no podrás crear indicadores
- Un mismo indicador puede pertenecer a varios RA con pesos distintos en cada uno
- El **peso** indica la importancia relativa del indicador dentro de cada RA
- Los indicadores se ordenan alfabéticamente por código
- La pestaña de Actividades se actualiza automáticamente al crear, editar o eliminar indicadores
