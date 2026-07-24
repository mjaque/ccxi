[← Volver al índice](indice.md)

# Gestión de Módulos — ccxi

## 5.1 Concepto

Un **módulo** en CCxI equivale a un curso, asignatura o grupo. Cada módulo es independiente, con sus propios estudiantes, resultados de aprendizaje, indicadores, actividades y calificaciones. Puedes tener todos los cursos y grupos que necesites sin que los datos se mezclen.

## 5.2 Crear un módulo

Desde el **panel superior**, visible en todas las pantallas:

1. Escribe el nombre del nuevo módulo en el campo de texto
2. Pulsa el botón **Crear**

El nombre no puede contener barras (`/`, `\`) ni caracteres especiales. Si el nombre ya existe, el sistema lo rechazará.

Si todo es correcto, el módulo se selecciona automáticamente y el resto de pestañas se recargan para trabajar con él.

## 5.3 Seleccionar un módulo

El desplegable del panel superior muestra todos los módulos disponibles. Al cambiar de módulo, todas las pestañas (Estudiantes, Resultados, Indicadores, Actividades, Calificaciones, Informes) se recargan automáticamente con los datos del módulo seleccionado. No es necesario recargar la página.

## 5.4 Bloqueo durante operaciones

Mientras se crea o recarga un módulo, el panel permanece bloqueado para evitar errores.

## 5.5 Eliminar un módulo

No hay opción para eliminar módulos desde la interfaz. Para eliminar un módulo, borra manualmente el archivo `data/<nombre>.sqlite` del sistema de archivos.
