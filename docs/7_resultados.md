[← Volver al índice](indice.md)

# Gestión de Resultados de Aprendizaje — ccxi

## 7.1 Acceso

Ve a la pestaña **Resultados**. Se muestra un formulario con los campos **Código**, **Nombre** y **Peso**, y una tabla con el listado de resultados de aprendizaje (RA) del módulo activo. Si aún no hay RA, la tabla muestra el mensaje "No hay resultados de aprendizaje registrados en este módulo."

## 7.2 Crear un resultado de aprendizaje

1. Rellena los campos:
   - **Código** (mínimo 3 caracteres, no puede repetirse)
   - **Nombre** (mínimo 3 caracteres)
   - **Peso** (número entero, debe ser 0 o mayor)
2. Pulsa **Guardar**

Si algún campo no cumple los requisitos, el sistema lo notificará antes de guardar.

## 7.3 Editar un resultado de aprendizaje

1. Pulsa el botón **Editar** en la fila correspondiente de la tabla
2. Los datos se cargan en el formulario y aparece el botón **Cancelar edición**
3. Modifica los campos necesarios y pulsa **Guardar**

Para cancelar la edición, pulsa **Cancelar edición**.

## 7.4 Eliminar un resultado de aprendizaje

1. Pulsa el botón **Eliminar** en la fila correspondiente
2. Se muestra un cuadro de confirmación
3. Confirma la eliminación

Si el RA tiene indicadores asociados, el sistema impedirá la eliminación y mostrará un aviso. Elimina primero los indicadores que dependan de él o desvincúlalos antes de borrar el RA.

## 7.5 Cambio de módulo

Al seleccionar otro módulo en el panel superior, la lista de resultados de aprendizaje se recarga automáticamente.

## 7.6 Observaciones

- El **código** debe ser único dentro del módulo
- El **peso** indica la importancia relativa del RA en la calificación final del módulo
- Los RA se ordenan alfabéticamente por código
- La pestaña de Indicadores se actualiza automáticamente al crear, editar o eliminar RA
